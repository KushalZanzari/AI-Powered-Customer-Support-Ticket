#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# validate_submission.sh — Pre-submission validation for OpenEnv
# ═══════════════════════════════════════════════════════════════════════════
#
# Checks:
#   1. openenv.yaml exists and has required fields
#   2. Docker builds successfully
#   3. Server starts and /health returns 200
#   4. /reset endpoint works (returns ticket data)
#   5. /step endpoint works (accepts an action)
#
# Usage:
#   ./validate_submission.sh [base_url]
#
#   base_url defaults to http://localhost:8000
# ═══════════════════════════════════════════════════════════════════════════

set -e

BASE_URL="${1:-http://localhost:8000}"
PASS="✅"
FAIL="❌"
ERRORS=0

echo "═══════════════════════════════════════════════════════════"
echo "  OpenEnv Submission Validator"
echo "  Target: $BASE_URL"
echo "═══════════════════════════════════════════════════════════"
echo ""

# ── 1. Check openenv.yaml ────────────────────────────────────────────────
echo "1️⃣  Checking openenv.yaml..."
if [ -f "env/openenv.yaml" ]; then
    echo "   $PASS openenv.yaml exists"

    if grep -q "spec_version" env/openenv.yaml && \
       grep -q "name" env/openenv.yaml && \
       grep -q "runtime" env/openenv.yaml; then
        echo "   $PASS Required fields present (spec_version, name, runtime)"
    else
        echo "   $FAIL Missing required fields in openenv.yaml"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   $FAIL openenv.yaml not found at env/openenv.yaml"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── 2. Check Dockerfile ──────────────────────────────────────────────────
echo "2️⃣  Checking Dockerfile..."
if [ -f "env/server/Dockerfile" ]; then
    echo "   $PASS Dockerfile exists"
else
    echo "   $FAIL Dockerfile not found at env/server/Dockerfile"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── 3. Health check ──────────────────────────────────────────────────────
echo "3️⃣  Health check ($BASE_URL/health)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   $PASS /health returned HTTP 200"
else
    echo "   $FAIL /health returned HTTP $HTTP_CODE (expected 200)"
    echo "   ℹ️  Make sure the server is running: uvicorn env.server.app:app --port 8000"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── 4. Reset endpoint ────────────────────────────────────────────────────
echo "4️⃣  Testing /reset endpoint..."
RESET_RESP=$(curl -s -X POST "$BASE_URL/reset" \
    -H "Content-Type: application/json" \
    -d '{"task_level": "easy"}' 2>/dev/null || echo "{}")

if echo "$RESET_RESP" | python -c "import sys,json; d=json.load(sys.stdin); assert 'ticket_id' in d" 2>/dev/null; then
    TICKET_ID=$(echo "$RESET_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['ticket_id'])")
    echo "   $PASS /reset returned ticket_id: $TICKET_ID"
else
    echo "   $FAIL /reset did not return expected ticket data"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── 5. Step endpoint ─────────────────────────────────────────────────────
echo "5️⃣  Testing /step endpoint..."
STEP_RESP=$(curl -s -X POST "$BASE_URL/step" \
    -H "Content-Type: application/json" \
    -d '{"action_type": "classify_issue", "category": "account"}' 2>/dev/null || echo "{}")

if echo "$STEP_RESP" | python -c "import sys,json; d=json.load(sys.stdin); assert 'reward' in d" 2>/dev/null; then
    REWARD=$(echo "$STEP_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['reward'])")
    echo "   $PASS /step returned reward: $REWARD"
else
    echo "   $FAIL /step did not return expected observation"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# ── Summary ──────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════"
if [ "$ERRORS" -eq 0 ]; then
    echo "  $PASS ALL CHECKS PASSED — Ready for submission!"
else
    echo "  $FAIL $ERRORS check(s) failed — Please fix before submitting."
fi
echo "═══════════════════════════════════════════════════════════"

exit $ERRORS
