from __future__ import annotations
import sqlite3
import threading
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

LogFn = Callable[[str, str], None]

def thread_safe_log_fn(db_path: str) -> LogFn:
    """Creates an independent DB connection per thread execution to eliminate SQLite thread crashes."""
    def _log(agent: str, message: str) -> None:
        try:
            with sqlite3.connect(db_path, timeout=10.0) as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS agent_chatter (message_id INTEGER PRIMARY KEY AUTOINCREMENT, agent TEXT, message TEXT, timestamp TEXT)"
                )
                conn.execute(
                    "INSERT INTO agent_chatter (agent, message, timestamp) VALUES (?, ?, ?)",
                    (agent, message, _utcnow_iso()),
                )
                conn.commit()
        except Exception:
            pass
    return _log

@dataclass
class JobSpec:
    name: str
    func: Callable[[], None]
    interval_seconds: float
    max_retries: int = 3
    backoff_base_seconds: float = 2.0
    run_at_start: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _next_run_at: float = field(default=0.0, repr=False)

class JobScheduler:
    def __init__(self, log_fn: Optional[LogFn] = None, tick_interval_seconds: float = 1.0) -> None:
        self._jobs: dict[str, JobSpec] = {}
        self._log = log_fn or (lambda agent, msg: None)
        self._tick_interval = tick_interval_seconds
        self._paused = threading.Event()
        self._stopped = threading.Event()
        self._stopped.set()
        self._poll_thread: Optional[threading.Thread] = None

    def register_job(self, name: str, func: Callable[[], None], interval_seconds: float, max_retries: int = 3, backoff_base_seconds: float = 2.0, run_at_start: bool = False) -> None:
        if name in self._jobs: raise ValueError(f"job {name!r} already registered")
        spec = JobSpec(name=name, func=func, interval_seconds=interval_seconds, max_retries=max_retries, backoff_base_seconds=backoff_base_seconds, run_at_start=run_at_start)
        spec._next_run_at = time.monotonic() if run_at_start else (time.monotonic() + interval_seconds)
        self._jobs[name] = spec

    def start(self) -> None:
        if not self._stopped.is_set(): return
        self._stopped.clear()
        self._poll_thread = threading.Thread(target=self._poll_loop, name="juicer-scheduler", daemon=True)
        self._poll_thread.start()
        self._log("Claude", "Scheduler started.")

    def pause(self) -> None:
        self._paused.set()
        self._log("Claude", "Scheduler paused (kill switch engaged).")

    def resume(self) -> None:
        self._paused.clear()
        self._log("Claude", "Scheduler resumed.")

    @property
    def is_paused(self) -> bool: return self._paused.is_set()
    @property
    def is_running(self) -> bool: return not self._stopped.is_set()

    def get_job_statuses(self) -> list[dict]:
        now = time.monotonic()
        return [{"name": name, "interval": spec.interval_seconds, "secs_until_next": max(0, int(spec._next_run_at - now))} for name, spec in self._jobs.items()]

    def _poll_loop(self) -> None:
        while not self._stopped.is_set():
            if not self._paused.is_set():
                now = time.monotonic()
                for spec in list(self._jobs.values()):
                    if now >= spec._next_run_at:
                        self._dispatch(spec)
            self._stopped.wait(self._tick_interval)

    def _dispatch(self, spec: JobSpec) -> None:
        if not spec._lock.acquire(blocking=False):
            self._log("Claude", f"Skipped job {spec.name!r}: previous run still active.")
            spec._next_run_at = time.monotonic() + spec.interval_seconds
            return
        spec._next_run_at = time.monotonic() + spec.interval_seconds
        threading.Thread(target=self._run_with_retry, args=(spec,), daemon=True).start()

    def _run_with_retry(self, spec: JobSpec) -> None:
        try:
            attempt = 0
            while True:
                attempt += 1
                try:
                    spec.func()
                    self._log("Claude", f"Job {spec.name!r} completed successfully (attempt {attempt}).")
                    return
                except Exception:
                    err = traceback.format_exc(limit=2).strip().splitlines()[-1]
                    if attempt > spec.max_retries:
                        self._log("Claude", f"Job {spec.name!r} failed permanently: {err}")
                        return
                    backoff = spec.backoff_base_seconds * (2 ** (attempt - 1))
                    time.sleep(backoff)
        finally:
            spec._lock.release()