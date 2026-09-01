#!/usr/bin/env bash
set -euo pipefail
: "${KNOWN_GOOD_GIT_SHA:?}"
echo "Rollback must redeploy the exact known-good immutable artifact/release manifest."
echo "Known-good Git SHA: $KNOWN_GOOD_GIT_SHA"
