# -*- coding: utf-8 -*-
def validate_slip(players, platform):
    errors = []
    num_legs = len(players)
    teams = list(set([p.get('team', 'UNK') for p in players]))
    
    if platform == "prizepicks":
        if num_legs < 2 or num_legs > 6: errors.append(f"PrizePicks: 2-6 legs required, got {num_legs}")
    elif platform == "underdog":
        if num_legs < 2 or num_legs > 8: errors.append(f"Underdog: 2-8 legs required, got {num_legs}")
    
    if len(teams) < 2 and platform in ["prizepicks", "underdog"]:
        errors.append(f"Multi-team required, got {len(teams)}")
    
    break_even = {
        "prizepicks": [0.545, 0.571, 0.586, 0.595, 0.599, 0.602],
        "underdog": [0.549, 0.571, 0.586, 0.595, 0.599, 0.602, 0.605, 0.607]
    }
    
    be_rate = 0.60
    if platform in break_even:
        idx = num_legs - 2
        if 0 <= idx < len(break_even[platform]):
            be_rate = break_even[platform][idx]
            
    return {"valid": len(errors) == 0, "errors": errors, "break_even_pct": round(be_rate * 100, 1)}

def calculate_correlated_fair_prob(legs):
    """
    Adjusts fair probability based on game script correlation.
    Example: QB Pass Yds + WR Rec Yds (Same Team) = Positive Correlation (+15% bump)
    """
    base_hit_rate = 0.52 # Standard assumed leg hit rate
    raw_prob = base_hit_rate ** len(legs)
    
    # Simple correlation detection logic
    qbs = [leg for leg in legs if "Pass" in leg[1] or "QB" in leg[0]]
    pass_catchers = [leg for leg in legs if "Rec" in leg[1]]
    
    correlation_modifier = 1.0
    if len(qbs) > 0 and len(pass_catchers) > 0:
        # Detected a stack (Positive Correlation)
        correlation_modifier = 1.15
    elif len(legs) >= 6:
        # Massive lottery tickets usually suffer from uncorrelated variance drop-off
        correlation_modifier = 0.85
        
    adjusted_prob = raw_prob * correlation_modifier
    return f"{max(0.1, adjusted_prob * 100):.1f}%"
