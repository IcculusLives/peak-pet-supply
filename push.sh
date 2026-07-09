#!/bin/bash
# Commit & push whatever is in ~/code/peak-pet-supply (Claude writes files here directly — no iCloud in the loop)
set -u
cd "$HOME/code/peak-pet-supply" || { echo "STOP: repo not found"; exit 1; }
git add -A
git -c user.name="Casey Conn" -c user.email="khanmsu@gmail.com" commit -q -m "site update $(date +%Y-%m-%d_%H%M)" || { echo "Nothing new to push."; exit 0; }
git push || { echo "STOP: push failed"; exit 1; }
echo "Pushed. Live in ~1 min: https://icculuslives.github.io/peak-pet-supply/"
