from __future__ import annotations
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable, Optional

Source = str
_VALID_SOURCES = {"DFS", "PARLAY", "PICKEM"}
_PLATFORM_TO_SOURCE = {
    "PRIZEPICKS": "PICKEM",
    "UNDERDOG": "PICKEM",
    "SPORTSBOOK_PARLAY": "PARLAY",
}

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

class RecommendationEngineError(ValueError):
    pass

@dataclass
class Leg:
    player_name: str
    stat_category: str
    line: float
    direction: str  # 'OVER' | 'UNDER'
    predicted_value: float

    def __post_init__(self) -> None:
        if self.direction not in ("OVER", "UNDER"):
            raise RecommendationEngineError(f"leg direction must be OVER or UNDER, got {self.direction!r}")

@dataclass
class GradeResult:
    source: Source
    reference_id: int
    hit_flag: Optional[int]
    legs_hit: Optional[int] = None
    leg_count: Optional[int] = None

class RecommendationEngine:
    def __init__(self, conn: sqlite3.Connection, on_grade: Optional[Callable[[GradeResult], None]] = None) -> None:
        self._conn = conn
        self._on_grade = on_grade
        self._require_tables()

    def _require_tables(self) -> None:
        cur = self._conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('slips', 'bet_grading', 'dfs_classic_lineups')")
        found = {row[0] for row in cur.fetchall()}
        missing = {"slips", "bet_grading"} - found
        if missing:
            raise RecommendationEngineError(f"Missing tables {sorted(missing)} - run db_migration.py first.")

    def record_dfs_lineup(self, lineup_type: str, projected_pts: float, roster: list[dict]) -> int:
        if projected_pts < 0: raise RecommendationEngineError("projected_pts cannot be negative")
        if not roster: raise RecommendationEngineError("roster cannot be empty")
        cur = self._conn.execute(
            "INSERT INTO dfs_classic_lineups (lineup_type, projected_pts, roster_json) VALUES (?, ?, ?)",
            (lineup_type, projected_pts, json.dumps(roster)),
        )
        self._conn.commit()
        return cur.lastrowid

    def record_slip(self, platform: str, legs: Iterable[Leg], implied_probability: Optional[float] = None, confidence_tier: Optional[str] = None) -> int:
        legs = list(legs)
        if platform not in _PLATFORM_TO_SOURCE:
            raise RecommendationEngineError(f"platform must be one of {sorted(_PLATFORM_TO_SOURCE)}")
        leg_count = len(legs)
        if not (2 <= leg_count <= 6):
            raise RecommendationEngineError(f"slips must have 2-6 legs, got {leg_count}")
        legs_json = json.dumps([leg.__dict__ for leg in legs])
        cur = self._conn.execute(
            "INSERT INTO slips (platform, leg_count, legs_json, implied_probability, confidence_tier, status, created_at) VALUES (?, ?, ?, ?, ?, 'PENDING', ?)",
            (platform, leg_count, legs_json, implied_probability, confidence_tier, _utcnow()),
        )
        self._conn.commit()
        return cur.lastrowid

    def grade_dfs_lineup(self, lineup_id: int, actual_pts: float) -> GradeResult:
        row = self._conn.execute("SELECT projected_pts FROM dfs_classic_lineups WHERE id = ?", (lineup_id,)).fetchone()
        if row is None: raise RecommendationEngineError(f"no dfs lineup with id={lineup_id}")
        projected_pts = row[0]
        hit_flag = 1 if actual_pts >= projected_pts else 0
        graded_at = _utcnow()

        self._conn.execute("UPDATE dfs_classic_lineups SET actual_pts = ?, graded_at = ? WHERE id = ?", (actual_pts, graded_at, lineup_id))
        self._conn.execute(
            "INSERT INTO bet_grading (source, reference_id, predicted_value, actual_value, hit_flag, created_at, graded_at) VALUES ('DFS', ?, ?, ?, ?, ?, ?)",
            (lineup_id, projected_pts, actual_pts, hit_flag, graded_at, graded_at),
        )
        self._conn.commit()
        result = GradeResult(source="DFS", reference_id=lineup_id, hit_flag=hit_flag)
        if self._on_grade: self._on_grade(result)
        return result

    def grade_slip(self, slip_id: int, leg_outcomes: list[tuple[str, float]]) -> GradeResult:
        row = self._conn.execute("SELECT platform, leg_count, legs_json FROM slips WHERE id = ?", (slip_id,)).fetchone()
        if row is None: raise RecommendationEngineError(f"no slip with id={slip_id}")
        platform, leg_count, legs_json = row
        legs = json.loads(legs_json)
        if len(leg_outcomes) != leg_count: raise RecommendationEngineError("leg outcome count mismatch")

        source = _PLATFORM_TO_SOURCE[platform]
        graded_at = _utcnow()
        legs_hit = 0

        for leg, (player_name, actual_value) in zip(legs, leg_outcomes):
            hit = actual_value >= leg["line"] if leg["direction"] == "OVER" else actual_value <= leg["line"]
            leg_hit_flag = 1 if hit else 0
            legs_hit += leg_hit_flag
            self._conn.execute(
                "INSERT INTO bet_grading (source, reference_id, player_name, stat_category, predicted_value, actual_value, hit_flag, leg_count, created_at, graded_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (source, slip_id, player_name, leg["stat_category"], leg["predicted_value"], actual_value, leg_hit_flag, leg_count, graded_at, graded_at),
            )

        slip_hit_flag = 1 if legs_hit == leg_count else 0
        self._conn.execute("UPDATE slips SET status = 'GRADED', legs_hit = ?, graded_at = ? WHERE id = ?", (legs_hit, graded_at, slip_id))
        self._conn.commit()
        result = GradeResult(source=source, reference_id=slip_id, hit_flag=slip_hit_flag, legs_hit=legs_hit, leg_count=leg_count)
        if self._on_grade: self._on_grade(result)
        return result