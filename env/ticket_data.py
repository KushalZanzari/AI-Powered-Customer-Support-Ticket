"""
Ticket database for the Customer Support Environment.

Contains curated, realistic support ticket scenarios organised by
difficulty level (easy / medium / hard).  Each ticket dict carries all
the information the environment and graders need.
"""

from typing import List, Dict, Any


# ═══════════════════════════════════════════════════════════════════════════
# EASY TICKETS — Task 1: Basic FAQ Resolution
# ═══════════════════════════════════════════════════════════════════════════
# Goal: Provide the correct answer in a single reply.
# Grading: keyword match + correct resolution.

EASY_TICKETS: List[Dict[str, Any]] = [
    {
        "ticket_id": "EASY-001",
        "ticket_text": (
            "Hi, I forgot my password and I can't log in to my account. "
            "Can you help me reset it?"
        ),
        "customer_name": "Alice Johnson",
        "customer_priority": "medium",
        "customer_history": ["Previous login issue 3 months ago"],
        "expected_category": "account",
        "expected_resolution_keywords": [
            "reset", "password", "link", "email", "settings", "forgot",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Help the customer reset their password. Classify the issue, "
            "then reply with clear password-reset instructions and resolve."
        ),
        "ideal_reply": (
            "You can reset your password by clicking 'Forgot Password' on the "
            "login page. A reset link will be sent to your registered email. "
            "If you don't receive it within 5 minutes, check your spam folder."
        ),
    },
    {
        "ticket_id": "EASY-002",
        "ticket_text": (
            "What are the pricing plans available? I'm looking for a plan "
            "suitable for a small team of 5 people."
        ),
        "customer_name": "Bob Smith",
        "customer_priority": "low",
        "customer_history": [],
        "expected_category": "general",
        "expected_resolution_keywords": [
            "plan", "pricing", "team", "starter", "business", "enterprise",
            "month", "annual", "per user",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Provide pricing information for the small-team plan. Classify "
            "the issue, reply with plan details, and resolve."
        ),
        "ideal_reply": (
            "We offer three plans: Starter ($9/user/month), Business "
            "($19/user/month) with priority support, and Enterprise (custom "
            "pricing). For a team of 5, the Business plan is most popular. "
            "Visit our pricing page for full details."
        ),
    },
    {
        "ticket_id": "EASY-003",
        "ticket_text": (
            "How do I export my data from the platform? I need a CSV file "
            "of my project history."
        ),
        "customer_name": "Carol Davis",
        "customer_priority": "low",
        "customer_history": [],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "export", "csv", "download", "settings", "data", "file",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Explain how to export data as CSV. Classify the issue, "
            "provide step-by-step instructions, and resolve."
        ),
        "ideal_reply": (
            "To export your data: 1) Go to Settings > Data Management, "
            "2) Click 'Export Data', 3) Select CSV format, 4) Choose the "
            "date range, 5) Click 'Download'. The file will be emailed to "
            "you within a few minutes."
        ),
    },
    {
        "ticket_id": "EASY-004",
        "ticket_text": (
            "I want to update the email address on my account. My current "
            "email is old and I need to change it to a new one."
        ),
        "customer_name": "David Wilson",
        "customer_priority": "medium",
        "customer_history": ["Account created 2 years ago"],
        "expected_category": "account",
        "expected_resolution_keywords": [
            "email", "update", "change", "profile", "settings", "account",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Help the customer update their email address. Classify the "
            "issue, provide instructions, and resolve."
        ),
        "ideal_reply": (
            "To update your email: Go to Profile > Account Settings > "
            "Email Address. Click 'Change Email', enter your new email, "
            "and confirm via the verification link sent to both your old "
            "and new email addresses."
        ),
    },
    {
        "ticket_id": "EASY-005",
        "ticket_text": (
            "Can I cancel my subscription? I won't be needing the service "
            "anymore after this month."
        ),
        "customer_name": "Eva Martinez",
        "customer_priority": "low",
        "customer_history": ["Subscribed for 6 months"],
        "expected_category": "billing",
        "expected_resolution_keywords": [
            "cancel", "subscription", "billing", "end", "refund", "renewal",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Assist the customer with subscription cancellation. Classify "
            "the issue, explain the process, and resolve."
        ),
        "ideal_reply": (
            "You can cancel your subscription from Settings > Billing > "
            "Manage Subscription > Cancel Plan. Your access will continue "
            "until the end of the current billing period. No further "
            "charges will be made."
        ),
    },
    {
        "ticket_id": "EASY-006",
        "ticket_text": (
            "Where can I find the API documentation? I'm a developer and "
            "I need to integrate your service into my app."
        ),
        "customer_name": "Frank Lee",
        "customer_priority": "low",
        "customer_history": [],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "api", "documentation", "docs", "developer", "integration",
            "endpoint", "reference",
        ],
        "expected_escalation_team": None,
        "goal": (
            "Direct the customer to the API documentation. Classify the "
            "issue, provide the link and a quick overview, and resolve."
        ),
        "ideal_reply": (
            "Our API documentation is available at docs.example.com/api. "
            "It includes quickstart guides, endpoint references, "
            "authentication details, and code samples in Python, "
            "JavaScript, and cURL. You can also generate an API key from "
            "Settings > Developer > API Keys."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# MEDIUM TICKETS — Task 2: Multi-step Issue Handling
# ═══════════════════════════════════════════════════════════════════════════
# Goal: Classify  →  Ask clarification  →  Provide solution  →  Resolve
# Grading: sequence correctness + partial scoring.

MEDIUM_TICKETS: List[Dict[str, Any]] = [
    {
        "ticket_id": "MED-001",
        "ticket_text": (
            "I was charged twice for my last month's subscription. "
            "The amounts are $19 each and I only have one account. "
            "Please look into this."
        ),
        "customer_name": "Grace Kim",
        "customer_priority": "high",
        "customer_history": [
            "Subscribed for 1 year",
            "Upgraded plan 2 months ago",
        ],
        "expected_category": "billing",
        "expected_resolution_keywords": [
            "refund", "duplicate", "charge", "billing", "credit",
            "processed", "investigation",
        ],
        "clarification_keywords": [
            "transaction", "date", "payment method", "receipt",
            "bank statement", "confirm",
        ],
        "expected_escalation_team": "billing_team",
        "goal": (
            "Resolve a duplicate billing charge. Classify the issue, "
            "ask for transaction details, provide a solution (refund or "
            "credit), and resolve."
        ),
        "ideal_reply": (
            "I've confirmed the duplicate charge on your account. A refund "
            "of $19 has been initiated and will appear in your account "
            "within 5-7 business days. I've also flagged this to prevent "
            "future occurrences."
        ),
        "expected_sequence": [
            "classify_issue",
            "request_more_info",
            "reply",
            "resolve",
        ],
    },
    {
        "ticket_id": "MED-002",
        "ticket_text": (
            "My dashboard keeps showing a 'connection error' whenever I "
            "try to load the analytics page. This started happening "
            "yesterday. Other pages work fine."
        ),
        "customer_name": "Henry Chen",
        "customer_priority": "high",
        "customer_history": [
            "Power user – logs in daily",
            "Previous API issue 1 month ago",
        ],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "cache", "clear", "browser", "refresh", "update", "fix",
            "resolved", "working",
        ],
        "clarification_keywords": [
            "browser", "device", "network", "screenshot", "error message",
            "version", "operating system",
        ],
        "expected_escalation_team": "technical_team",
        "goal": (
            "Diagnose and fix the dashboard connection error. Classify, "
            "gather diagnostics, provide a fix, and resolve."
        ),
        "ideal_reply": (
            "This is a known issue affecting the analytics module after "
            "yesterday's update. Please clear your browser cache and "
            "hard-refresh (Ctrl+Shift+R). If the issue persists, try "
            "using an incognito window. Our team has deployed a fix."
        ),
        "expected_sequence": [
            "classify_issue",
            "request_more_info",
            "reply",
            "resolve",
        ],
    },
    {
        "ticket_id": "MED-003",
        "ticket_text": (
            "I'd like to upgrade my plan from Starter to Business, but "
            "I need to know how the billing transition works. Will I be "
            "charged the full price immediately or prorated?"
        ),
        "customer_name": "Irene Patel",
        "customer_priority": "medium",
        "customer_history": ["Starter plan for 4 months"],
        "expected_category": "billing",
        "expected_resolution_keywords": [
            "upgrade", "prorate", "prorated", "charge", "billing cycle",
            "difference", "immediately",
        ],
        "clarification_keywords": [
            "current plan", "billing date", "payment method", "annual",
            "monthly",
        ],
        "expected_escalation_team": "billing_team",
        "goal": (
            "Explain the plan upgrade billing process. Classify, clarify "
            "billing cycle, explain prorating, and resolve."
        ),
        "ideal_reply": (
            "When you upgrade, you'll only be charged the prorated "
            "difference for the remaining days in your current billing "
            "cycle. Starting next cycle, you'll be billed at the full "
            "Business plan rate of $19/user/month."
        ),
        "expected_sequence": [
            "classify_issue",
            "request_more_info",
            "reply",
            "resolve",
        ],
    },
    {
        "ticket_id": "MED-004",
        "ticket_text": (
            "I'm unable to add new team members to my workspace. When I "
            "click 'Invite', nothing happens. I've tried different "
            "browsers but the issue persists."
        ),
        "customer_name": "James Rivera",
        "customer_priority": "high",
        "customer_history": [
            "Business plan user",
            "Team of 12 members",
        ],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "invite", "permission", "admin", "role", "seat", "limit",
            "workspace", "fixed",
        ],
        "clarification_keywords": [
            "role", "admin rights", "seat limit", "plan", "browser console",
            "error log",
        ],
        "expected_escalation_team": "technical_team",
        "goal": (
            "Fix the team invitation issue. Classify, check permissions "
            "and seat limits, provide a solution, and resolve."
        ),
        "ideal_reply": (
            "It looks like your workspace has reached its seat limit of 10 "
            "users on the Business plan. You can either upgrade to "
            "Enterprise for unlimited seats, or remove inactive members "
            "to free up slots. I've also verified your admin permissions "
            "are correctly set."
        ),
        "expected_sequence": [
            "classify_issue",
            "request_more_info",
            "reply",
            "resolve",
        ],
    },
    {
        "ticket_id": "MED-005",
        "ticket_text": (
            "I noticed my account was accessed from an unfamiliar IP "
            "address. I didn't log in from that location. Can you check "
            "if my account is compromised?"
        ),
        "customer_name": "Karen Thompson",
        "customer_priority": "high",
        "customer_history": [
            "2FA not enabled",
            "Last password change was 8 months ago",
        ],
        "expected_category": "account",
        "expected_resolution_keywords": [
            "security", "password", "2FA", "two-factor", "session",
            "revoke", "login history", "protect",
        ],
        "clarification_keywords": [
            "IP address", "location", "time", "activity log", "device",
        ],
        "expected_escalation_team": "security_team",
        "goal": (
            "Investigate potential unauthorized access. Classify, gather "
            "details, secure the account, and resolve."
        ),
        "ideal_reply": (
            "I've reviewed your login history and see the unfamiliar access. "
            "As a precaution: 1) I've revoked all active sessions, "
            "2) Please reset your password immediately, 3) Enable 2FA "
            "from Settings > Security. No data was modified during the "
            "suspicious session."
        ),
        "expected_sequence": [
            "classify_issue",
            "request_more_info",
            "reply",
            "resolve",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# HARD TICKETS — Task 3: Complex Escalation Case
# ═══════════════════════════════════════════════════════════════════════════
# Goal: Empathetic response → Classify → Escalate correctly → Resolve
# Grading: tone + correctness + escalation decision.

HARD_TICKETS: List[Dict[str, Any]] = [
    {
        "ticket_id": "HARD-001",
        "ticket_text": (
            "I AM EXTREMELY FRUSTRATED! I've been a loyal customer for "
            "3 YEARS and your service has been TERRIBLE lately. My data "
            "was LOST during the migration, my billing is WRONG — I've "
            "been overcharged for 2 months, AND nobody from your team "
            "has responded to my previous 3 support tickets! This is "
            "completely UNACCEPTABLE. Fix this NOW or I'm leaving!"
        ),
        "customer_name": "Michael Brown",
        "customer_priority": "critical",
        "customer_history": [
            "3-year customer",
            "Enterprise plan",
            "3 unresolved previous tickets",
            "Data migration participant",
        ],
        "expected_category": "billing",
        "expected_resolution_keywords": [
            "refund", "data", "restore", "priority", "manager",
            "compensation", "escalate",
        ],
        "empathy_keywords": [
            "sorry", "understand", "frustrating", "apologize",
            "appreciate", "patience", "valued", "inconvenience",
        ],
        "urgency_indicators": [
            "frustrated", "unacceptable", "leaving", "terrible",
            "now", "immediately", "3 years", "loyal",
        ],
        "expected_escalation_team": "management",
        "goal": (
            "Handle an angry, high-value customer with multiple issues. "
            "Respond empathetically, classify the primary issue, escalate "
            "to management, and work toward resolution."
        ),
        "ideal_reply": (
            "I sincerely apologize for the frustrating experience, "
            "Michael. As a valued 3-year customer, you deserve far better. "
            "I'm escalating your case to our management team immediately. "
            "In the meantime, I've flagged the billing overcharges for an "
            "immediate refund, and our data team will prioritize restoring "
            "your lost data."
        ),
        "expected_sequence": [
            "reply",             # Empathetic first
            "classify_issue",
            "escalate",
            "resolve",
        ],
    },
    {
        "ticket_id": "HARD-002",
        "ticket_text": (
            "Your platform crashed during my live product demo to a major "
            "client. Do you understand how embarrassing that was? I lost "
            "a $50,000 deal because your service went down. I need "
            "immediate compensation and an explanation. This CANNOT happen "
            "again. I'm considering legal action."
        ),
        "customer_name": "Sarah Williams",
        "customer_priority": "critical",
        "customer_history": [
            "Enterprise plan",
            "2-year customer",
            "Revenue-critical usage",
            "SLA agreement in place",
        ],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "SLA", "compensation", "uptime", "incident", "report",
            "prevent", "credit", "guarantee",
        ],
        "empathy_keywords": [
            "sorry", "understand", "deeply regret", "apologize",
            "embarrassing", "unacceptable", "acknowledge",
        ],
        "urgency_indicators": [
            "crashed", "live demo", "$50,000", "legal action",
            "immediately", "cannot happen",
        ],
        "expected_escalation_team": "management",
        "goal": (
            "Address a critical service outage that caused business loss. "
            "Empathize, classify, escalate to management for SLA review, "
            "and initiate compensation."
        ),
        "ideal_reply": (
            "I deeply regret the disruption during your demo, Sarah. This "
            "is completely unacceptable and I take full responsibility on "
            "behalf of our team. I'm escalating this to our VP of "
            "Engineering and Account Management immediately. We will "
            "provide a detailed incident report, SLA credit review, and "
            "discuss appropriate compensation within 24 hours."
        ),
        "expected_sequence": [
            "reply",
            "classify_issue",
            "escalate",
            "resolve",
        ],
    },
    {
        "ticket_id": "HARD-003",
        "ticket_text": (
            "I just found out that someone accessed my account and deleted "
            "all my project files. I have years of work stored on your "
            "platform and now EVERYTHING IS GONE. I'm panicking. I also "
            "noticed unauthorized charges on my billing. PLEASE help me "
            "immediately — this is my livelihood!"
        ),
        "customer_name": "Rachel Green",
        "customer_priority": "critical",
        "customer_history": [
            "5-year customer",
            "Large data storage user",
            "No 2FA enabled",
            "Freelance professional",
        ],
        "expected_category": "account",
        "expected_resolution_keywords": [
            "security", "restore", "backup", "recovery", "freeze",
            "investigate", "unauthorized", "protect",
        ],
        "empathy_keywords": [
            "sorry", "understand", "distressing", "help",
            "priority", "immediately", "safe", "secure",
        ],
        "urgency_indicators": [
            "deleted", "everything is gone", "panicking",
            "livelihood", "unauthorized", "immediately",
        ],
        "expected_escalation_team": "security_team",
        "goal": (
            "Handle a security breach with data loss and unauthorized "
            "charges. Empathize, classify, secure the account, escalate "
            "to security team, and initiate data recovery."
        ),
        "ideal_reply": (
            "I completely understand how distressing this is, Rachel, and "
            "I'm treating this as our highest priority. I've immediately "
            "frozen your account to prevent further unauthorized access. "
            "Our security team is being alerted right now. Your files may "
            "be recoverable from our backup system — I'm initiating that "
            "process. The unauthorized charges will be reversed."
        ),
        "expected_sequence": [
            "reply",
            "classify_issue",
            "escalate",
            "resolve",
        ],
    },
    {
        "ticket_id": "HARD-004",
        "ticket_text": (
            "We signed an annual enterprise contract 2 months ago and your "
            "team promised features that DON'T EXIST. The API rate limits "
            "are nothing like what we were told, the 'priority support' "
            "takes 48 hours to respond, and integration has been a "
            "nightmare. We feel MISLED. Our CTO is furious and wants to "
            "terminate the contract."
        ),
        "customer_name": "Thomas Anderson",
        "customer_priority": "critical",
        "customer_history": [
            "Enterprise annual contract",
            "2 months into contract",
            "Technical integration in progress",
            "Multiple stakeholders (CTO, Dev team)",
        ],
        "expected_category": "general",
        "expected_resolution_keywords": [
            "contract", "review", "account manager", "resolution",
            "commitment", "features", "roadmap", "escalate",
        ],
        "empathy_keywords": [
            "sorry", "understand", "valid concerns", "accountability",
            "hear you", "take seriously", "commitment",
        ],
        "urgency_indicators": [
            "misled", "terminate contract", "furious", "don't exist",
            "nightmare", "CTO",
        ],
        "expected_escalation_team": "management",
        "goal": (
            "Address enterprise contract dissatisfaction. Empathize, "
            "classify, escalate to management for contract review, and "
            "propose a path forward."
        ),
        "ideal_reply": (
            "Thomas, your concerns are completely valid and I take them "
            "very seriously. Feeling misled is unacceptable and I'm sorry "
            "you're experiencing this. I'm escalating directly to our VP "
            "of Sales and your dedicated Account Manager for an urgent "
            "contract review. We'll schedule a call with your CTO within "
            "48 hours to address every point."
        ),
        "expected_sequence": [
            "reply",
            "classify_issue",
            "escalate",
            "resolve",
        ],
    },
    {
        "ticket_id": "HARD-005",
        "ticket_text": (
            "My team has been experiencing intermittent outages every day "
            "for the past WEEK and your status page says everything is "
            "operational. I have screenshots and logs proving it. Are you "
            "hiding issues from your customers? Our entire development "
            "pipeline depends on your service. 15 engineers are blocked. "
            "We need this fixed TODAY."
        ),
        "customer_name": "Lisa Park",
        "customer_priority": "critical",
        "customer_history": [
            "Business plan",
            "1-year customer",
            "CI/CD pipeline integration",
            "15-engineer team",
        ],
        "expected_category": "technical",
        "expected_resolution_keywords": [
            "investigate", "logs", "incident", "priority", "fix",
            "team", "monitoring", "status", "transparency",
        ],
        "empathy_keywords": [
            "sorry", "understand", "frustrating", "unacceptable",
            "transparency", "seriously", "apologize",
        ],
        "urgency_indicators": [
            "week", "hiding", "15 engineers", "blocked",
            "today", "every day", "entire pipeline",
        ],
        "expected_escalation_team": "technical_team",
        "goal": (
            "Address persistent outages not reflected on the status page. "
            "Empathize, classify, escalate to the technical team, and "
            "commit to a resolution timeline."
        ),
        "ideal_reply": (
            "Lisa, I sincerely apologize for the ongoing disruptions. "
            "You're right to be frustrated — a week of outages blocking "
            "15 engineers is completely unacceptable. I'm escalating this "
            "to our infrastructure team as a P0 incident right now. We'll "
            "review your logs, update the status page transparently, and "
            "provide hourly updates until this is fully resolved."
        ),
        "expected_sequence": [
            "reply",
            "classify_issue",
            "escalate",
            "resolve",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Utility helpers
# ═══════════════════════════════════════════════════════════════════════════


def get_tickets_by_level(level: str) -> List[Dict[str, Any]]:
    """Return the ticket list for a given difficulty level."""
    mapping = {
        "easy": EASY_TICKETS,
        "medium": MEDIUM_TICKETS,
        "hard": HARD_TICKETS,
    }
    return mapping.get(level, EASY_TICKETS)


def get_all_tickets() -> Dict[str, List[Dict[str, Any]]]:
    """Return every ticket pool keyed by level."""
    return {
        "easy": EASY_TICKETS,
        "medium": MEDIUM_TICKETS,
        "hard": HARD_TICKETS,
    }
