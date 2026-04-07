"""Quick end-to-end test — uses seed=42 and correct actions for each ticket."""
import requests, json

BASE = "http://localhost:8000"

def test_task(level, actions):
    print(f"\n{'='*50}")
    print(f"  TASK: {level.upper()}")
    print(f"{'='*50}")
    r = requests.post(f"{BASE}/reset", json={"task_level": level, "seed": 42})
    obs = r.json()
    print(f"  Ticket: {obs['ticket_id']} - {obs['customer_name']}")
    print(f"  Priority: {obs['customer_priority']}")
    print(f"  Text: {obs['ticket_text'][:100]}...")

    for i, action in enumerate(actions, 1):
        r = requests.post(f"{BASE}/step", json=action)
        obs = r.json()
        print(f"  Step {i} ({action['action_type']}): reward={obs['reward']}, status={obs['ticket_status']}")
        if obs.get("done"):
            score = obs.get("metadata", {}).get("final_score", "N/A")
            print(f"  >>> FINAL SCORE: {score}")
            return score
    return 0.0

# First discover which tickets we get with seed=42
r = requests.post(f"{BASE}/reset", json={"task_level": "easy", "seed": 42})
easy_ticket = r.json()
print(f"Easy ticket preview: {easy_ticket['ticket_id']}")

r = requests.post(f"{BASE}/reset", json={"task_level": "medium", "seed": 42})
med_ticket = r.json()
print(f"Medium ticket preview: {med_ticket['ticket_id']}")

r = requests.post(f"{BASE}/reset", json={"task_level": "hard", "seed": 42})
hard_ticket = r.json()
print(f"Hard ticket preview: {hard_ticket['ticket_id']}")

# Easy: EASY-005 (billing - cancel subscription)
s1 = test_task("easy", [
    {"action_type": "classify_issue", "category": "billing"},
    {"action_type": "reply", "message": "You can cancel your subscription from Settings, then go to Billing, then Manage Subscription and Cancel Plan. Your access continues until the end of the billing period. No further renewal charges will be made."},
    {"action_type": "resolve"},
])

# Medium: MED-003 (billing - upgrade prorating)
s2 = test_task("medium", [
    {"action_type": "classify_issue", "category": "billing"},
    {"action_type": "request_more_info"},
    {"action_type": "reply", "message": "When you upgrade your plan, you will only be charged the prorated difference for the remaining days in your current billing cycle. The charge will be applied immediately. Starting next cycle you'll be billed at the full Business plan rate."},
    {"action_type": "resolve"},
])

# Hard: HARD-001 (billing - angry customer, management escalation)
s3 = test_task("hard", [
    {"action_type": "reply", "message": "I sincerely apologize for this frustrating experience. I completely understand how unacceptable this is. As a valued customer, you deserve far better. I am escalating this immediately to our management team as highest priority."},
    {"action_type": "classify_issue", "category": "billing"},
    {"action_type": "escalate", "team": "management"},
    {"action_type": "resolve"},
])

print(f"\n{'='*50}")
print(f"  RESULTS SUMMARY")
print(f"{'='*50}")
print(f"  Easy:   {s1}")
print(f"  Medium: {s2}")
print(f"  Hard:   {s3}")
avg = (float(s1 or 0) + float(s2 or 0) + float(s3 or 0)) / 3
print(f"  Avg:    {avg:.2f}")
print(f"{'='*50}")
