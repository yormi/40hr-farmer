#!/usr/bin/env bash
# End-to-end smoke test of the 40hr Farmer welcome funnel.
# Submits a tagged test contact, verifies contact + properties + marketing
# flag + Email 01 delivery, then cleans up. Run before pushing changes
# under email/ or anything that touches the workflow.
#
# See email/HUBSPOT-PROCEDURE.md for the underlying API details.

set -euo pipefail

PORTAL_ID="5156324"
FORM_ID="7f28cb26-8aea-432e-bf7f-c50a1484d0a3"
LANDING_URL="https://yormi.github.io/40hr-farmer/"
TIMESTAMP=$(date +%s)
TEST_EMAIL="guillaume+e2e+${TIMESTAMP}@orisha.io"
TEST_FIRSTNAME="E2E"
TEST_FARM="Smoke Test Farm"
TEST_DEAL="orisha;gfm"

# Load API token
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -z "${HUBSPOT_API_KEY:-}" ] && [ -f "${REPO_ROOT}/.secrets/hubspot.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.secrets/hubspot.env"
  set +a
fi
if [ -z "${HUBSPOT_API_KEY:-}" ]; then
  echo "ERROR: HUBSPOT_API_KEY not set (env or .secrets/hubspot.env)"
  exit 1
fi

CONTACT_ID=""
cleanup() {
  if [ -n "$CONTACT_ID" ]; then
    echo "  cleanup: deleting test contact $CONTACT_ID"
    curl -s -o /dev/null -X DELETE \
      -H "Authorization: Bearer $HUBSPOT_API_KEY" \
      "https://api.hubapi.com/crm/v3/objects/contacts/${CONTACT_ID}" || true
  fi
  rm -f /tmp/e2e-submit.json /tmp/e2e-contact.json /tmp/e2e-events.json
}
trap cleanup EXIT

echo "=== E2E test: 40hr Farmer welcome funnel ==="
echo "Test email: $TEST_EMAIL"
echo

# 1. Submit form via the public Forms Submissions endpoint
echo "1. Form submit..."
CODE=$(curl -s -o /tmp/e2e-submit.json -w "%{http_code}" -X POST \
  "https://api.hsforms.com/submissions/v3/integration/submit/${PORTAL_ID}/${FORM_ID}" \
  -H "Content-Type: application/json" \
  -d "{
    \"fields\": [
      {\"objectTypeId\":\"0-1\",\"name\":\"firstname\",\"value\":\"${TEST_FIRSTNAME}\"},
      {\"objectTypeId\":\"0-1\",\"name\":\"farm_name\",\"value\":\"${TEST_FARM}\"},
      {\"objectTypeId\":\"0-1\",\"name\":\"email\",\"value\":\"${TEST_EMAIL}\"},
      {\"objectTypeId\":\"0-1\",\"name\":\"forty_hour_farmer_deal\",\"value\":\"${TEST_DEAL}\"}
    ],
    \"context\":{\"pageUri\":\"${LANDING_URL}\",\"pageName\":\"40hr Farmer\"}
  }")
if [ "$CODE" != "200" ]; then
  echo "  FAIL: HTTP $CODE"
  cat /tmp/e2e-submit.json
  exit 1
fi
echo "  OK"

# 2. Poll for contact creation and verify properties (max 30s)
echo "2. Contact creation + properties..."
EMAIL_ENC=$(echo "$TEST_EMAIL" | sed 's/+/%2B/g; s/@/%40/g')
for _ in $(seq 1 15); do
  sleep 2
  CODE=$(curl -s -o /tmp/e2e-contact.json -w "%{http_code}" \
    -H "Authorization: Bearer $HUBSPOT_API_KEY" \
    "https://api.hubapi.com/crm/v3/objects/contacts/${EMAIL_ENC}?idProperty=email&properties=firstname,email,farm_name,forty_hour_farmer_deal,hs_marketable_status")
  [ "$CODE" = "200" ] && break
done
if [ "$CODE" != "200" ]; then
  echo "  FAIL: contact not found after 30s (last HTTP $CODE)"
  exit 1
fi

CONTACT_ID=$(jq -r '.id' /tmp/e2e-contact.json)
FIRSTNAME=$(jq -r '.properties.firstname' /tmp/e2e-contact.json)
FARM=$(jq -r '.properties.farm_name' /tmp/e2e-contact.json)
DEAL=$(jq -r '.properties.forty_hour_farmer_deal' /tmp/e2e-contact.json)
MARKETABLE=$(jq -r '.properties.hs_marketable_status' /tmp/e2e-contact.json)

FAILED=0
[ "$FIRSTNAME" = "$TEST_FIRSTNAME" ] || { echo "  FAIL: firstname=$FIRSTNAME"; FAILED=1; }
[ "$FARM" = "$TEST_FARM" ] || { echo "  FAIL: farm_name=$FARM"; FAILED=1; }
[ "$DEAL" = "$TEST_DEAL" ] || { echo "  FAIL: forty_hour_farmer_deal=$DEAL"; FAILED=1; }
[ "$MARKETABLE" = "true" ] || { echo "  FAIL: hs_marketable_status=$MARKETABLE (must be true)"; FAILED=1; }
[ "$FAILED" = "0" ] || exit 1
echo "  OK: contact $CONTACT_ID with all 4 properties + marketing flag"

# 3. Poll for Email 01 DELIVERED event (max 30s)
echo "3. Email delivery..."
DELIVERED=""
for _ in $(seq 1 15); do
  sleep 2
  curl -s \
    -H "Authorization: Bearer $HUBSPOT_API_KEY" \
    "https://api.hubapi.com/email/public/v1/events?recipient=${EMAIL_ENC}" > /tmp/e2e-events.json
  DELIVERED=$(jq -r '.events[] | select(.type == "DELIVERED") | .type' /tmp/e2e-events.json | head -1)
  [ "$DELIVERED" = "DELIVERED" ] && break
done
if [ "$DELIVERED" != "DELIVERED" ]; then
  echo "  FAIL: no DELIVERED event after 30s"
  jq '.events | map({type, recipient, created})' /tmp/e2e-events.json || true
  exit 1
fi
echo "  OK"

echo
echo "=== ALL CHECKS PASSED ==="
echo "Pipeline: form → contact → marketing → workflow → Email 01 DELIVERED"
