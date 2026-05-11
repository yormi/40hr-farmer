#!/usr/bin/env bash
# Push the current HEAD to the staging repo (yormi/40hr-farmer-staging)
# as its main branch. GitHub Pages on that repo auto-deploys, serving at
# https://yormi.github.io/40hr-farmer-staging/ within ~30-90s.
#
# Use this to preview any landing-page change before pushing to the production
# repo (yormi/40hr-farmer -> https://yormi.github.io/40hr-farmer/).
#
# Force-with-lease so any feature branch can become staging's main without
# fast-forward conflicts, but without clobbering parallel writes.

set -euo pipefail

BRANCH=$(git rev-parse --abbrev-ref HEAD)
STAGING_URL="https://yormi.github.io/40hr-farmer-staging/"

if ! git remote get-url staging >/dev/null 2>&1; then
  echo "No 'staging' remote configured. Run:"
  echo "  git remote add staging git@github.com:yormi/40hr-farmer-staging.git"
  exit 1
fi

echo "Pushing ${BRANCH} -> staging:main ..."
git push staging "${BRANCH}:main" --force-with-lease
echo ""
echo "Staging URL: ${STAGING_URL}"
echo "Deploy typically lands in 30-90s. Tail status with:"
echo "  gh api /repos/yormi/40hr-farmer-staging/pages | jq .status"
