"""Quick test of all endpoints after Pydantic migration."""
import requests
import json

BASE = "http://localhost:8000"

# 1. Health
r = requests.get(f"{BASE}/health")
print(f"HEALTH: {r.status_code} {r.json()}")
assert r.status_code == 200, "Health check failed"

# 2. Reset
r = requests.post(f"{BASE}/reset", json={"task_level": "easy", "seed": 42})
obs = r.json()
print(f"RESET: {r.status_code} ticket_id={obs['ticket_id']} done={obs['done']}")
assert r.status_code == 200, "Reset failed"
assert "ticket_id" in obs, "Missing ticket_id in reset response"

# 3. Step - classify
r = requests.post(f"{BASE}/step", json={"action_type": "classify_issue", "category": "billing"})
obs = r.json()
print(f"STEP1 (classify): {r.status_code} reward={obs['reward']} status={obs['ticket_status']}")
assert r.status_code == 200, "Step classify failed"
assert "reward" in obs, "Missing reward"

# 4. Step - reply
r = requests.post(f"{BASE}/step", json={
    "action_type": "reply",
    "message": "You can cancel your subscription from Settings, Billing, Manage Subscription. No further renewal charges will be made."
})
obs = r.json()
print(f"STEP2 (reply): {r.status_code} reward={obs['reward']} status={obs['ticket_status']}")

# 5. Step - resolve
r = requests.post(f"{BASE}/step", json={"action_type": "resolve"})
obs = r.json()
final_score = obs.get("metadata", {}).get("final_score", "N/A")
print(f"STEP3 (resolve): {r.status_code} reward={obs['reward']} done={obs['done']} final_score={final_score}")
assert obs["done"] == True, "Episode should be done after resolve"
assert isinstance(final_score, (int, float)), "final_score should be numeric"
assert 0.0 <= final_score <= 1.0, f"final_score {final_score} out of range"

# 6. State
r = requests.get(f"{BASE}/state")
state = r.json()
print(f"STATE: {r.status_code} keys={list(state.keys())}")
assert r.status_code == 200, "State endpoint failed"
assert "episode_id" in state, "Missing episode_id in state"

# 7. Test all 3 task levels
for level in ["easy", "medium", "hard"]:
    r = requests.post(f"{BASE}/reset", json={"task_level": level, "seed": 42})
    obs = r.json()
    assert obs["current_task"] == level, f"Expected task {level}, got {obs['current_task']}"
    print(f"TASK {level}: ticket_id={obs['ticket_id']} priority={obs['customer_priority']}")

print("\n" + "=" * 50)
print("  ALL ENDPOINT TESTS PASSED!")
print("=" * 50)
