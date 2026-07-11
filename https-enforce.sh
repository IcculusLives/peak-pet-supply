#!/bin/bash
# Final domain-flip step: turn on Enforce HTTPS once GitHub's cert is ready. Safe to re-run. Self-deletes on success.
set -u
STATE=$(gh api repos/IcculusLives/peak-pet-supply/pages --jq '.https_certificate.state' 2>/dev/null || echo "unknown")
echo "Certificate state: $STATE"
if [ "$STATE" = "approved" ] || [ "$STATE" = "issued" ]; then
  gh api -X PUT repos/IcculusLives/peak-pet-supply/pages -F https_enforced=true >/dev/null \
    && echo "HTTPS enforced. https://www.peakpetsupply.com is fully live & secure." \
    && rm -f "$HOME/code/peak-pet-supply/https-enforce.sh" \
    && echo "(script self-deleted)"
else
  echo "Cert not ready yet — totally normal, takes up to ~1 hour after the DNS flip."
  echo "Just run this same paste again later."
fi
