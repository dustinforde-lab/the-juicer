import json, sys

print("🩺 [QA & HEALING] Deploying Dwight & Dr. Love...")

def dwight_inspect(ticket):
    # Dwight's strict clipboard checklist
    required = ["player", "team", "stat", "line"]
    for req in required:
        if req not in ticket or not str(ticket[req]).strip():
            return False, f"Missing or empty: {req}"
    return True, "Passed"

def dr_love_heal(broken_ticket):
    # Dr. Love's surgical kit for common sportsbook API typos
    healed = {}
    mapping = {"athlete": "player", "squad": "team", "prop": "stat", "value": "line", "points": "line"}
    
    for key, val in broken_ticket.items():
        clean_key = mapping.get(key.lower(), key.lower())
        healed[clean_key] = val
        
    # Check if the stitched-up ticket passes Dwight
    passed, _ = dwight_inspect(healed)
    if passed:
        return healed
    else:
        # Safe fallback: The system never crashes, just shows awaiting data
        return {"player": "Awaiting Data", "team": "TBD", "stat": "System Sync", "line": "..."}

def run_chunk3_audit():
    print("\n🔍 RUNNING CHUNK 3 SELF-CHECK & AUDIT...")
    errors = []
    
    # Test 1: The Perfect Box
    good_box = {"player": "Amon-Ra", "team": "DET", "stat": "Yards", "line": "85.5"}
    passed, msg = dwight_inspect(good_box)
    if not passed: errors.append(f"Dwight rejected a good box: {msg}")
    
    # Test 2: The Broken Box (API changed 'player' to 'athlete')
    bad_box = {"athlete": "Jared Goff", "squad": "DET", "prop": "Yards", "value": "250.5"}
    passed, msg = dwight_inspect(bad_box)
    if passed: errors.append("Dwight accidentally passed a broken box.")
    
    # Test 3: The Surgery
    fixed_box = dr_love_heal(bad_box)
    passed, msg = dwight_inspect(fixed_box)
    if not passed: errors.append("Dr. Love failed to heal the broken box.")
    
    # Test 4: The Dead Box (Complete garbage data)
    dead_box = {"random_junk": 123}
    fallback_box = dr_love_heal(dead_box)
    passed, msg = dwight_inspect(fallback_box)
    if not passed: errors.append("Dr. Love failed to apply the safe fallback mask.")
    
    if errors:
        print("❌ AUDIT FAILED:")
        for err in errors: print(f"  -> {err}")
        sys.exit(1)
    else:
        print("✅ [PASS] Dwight: Successfully caught missing data labels.")
        print("✅ [PASS] Dr. Love: Successfully stitched broken API keys.")
        print("✅ [PASS] Fallback: Safe 'Awaiting Data' mask applied to dead feeds.")
        print("🎯 CHUNK 3 INTEGRITY VERIFIED. QA PIPELINE SECURE.")

if __name__ == "__main__":
    run_chunk3_audit()