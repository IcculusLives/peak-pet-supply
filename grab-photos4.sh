#!/bin/bash
# Round 4: grab anything that hit Messages in the last 6 hours (text yourself the 5 photos + dock video first!). Self-deletes on success.
set -u
DEST="$HOME/Downloads/peak-photos"; mkdir -p "$DEST"; COUNT=0
while IFS= read -r -d '' f; do cp -n "$f" "$DEST/" 2>/dev/null && COUNT=$((COUNT+1)); done < <(find "$HOME/Library/Messages/Attachments" -type f \( -iname '*.heic' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mov' -o -iname '*.mp4' \) -size +100k -mmin -360 -print0 2>/dev/null)
for h in "$DEST"/*.heic "$DEST"/*.HEIC; do [ -f "$h" ] || continue; sips -s format jpeg "$h" --out "${h%.*}.jpg" >/dev/null 2>&1 && rm -f "$h"; done
echo "Copied $COUNT new file(s)."
[ "$COUNT" -gt 0 ] && { rm -f "$HOME/code/peak-pet-supply/grab-photos4.sh"; echo "(script self-deleted)"; } || echo "(0 files — text them to yourself first, then re-paste)"
