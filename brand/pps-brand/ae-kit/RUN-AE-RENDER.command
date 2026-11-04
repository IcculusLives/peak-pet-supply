#!/bin/zsh
# RUN-AE-RENDER.command — queue + render PPS_Summit to ae-kit/renders (H.264 if a template exists, else ProRes/Lossless .mov).
# Usage:  zsh ~/code/peak-pet-supply/brand/pps-brand/ae-kit/RUN-AE-RENDER.command            # builds into whatever project is open (or a new one)
#         zsh …/RUN-AE-RENDER.command '/path/PPS_Summit.aep'                                    # opens that project first (refuses if a DIFFERENT unsaved project is open)
# Open After Effects first. If it hangs and dies with "-1712", AE has a modal dialog open: dismiss it and rerun. Progress → ae-kit/build-log.txt.
# AE must allow scripts to write files: Settings › Scripting & Expressions › "Allow Scripts to Write Files and Access Network" (CSD builds needed it too).
set -euo pipefail
AE_APP="Adobe After Effects 2026"
KIT="${0:A:h}"; AEP="${1:-}"
[[ -f "$KIT/render-h264.jsx" ]] || { echo "✗ no render-h264.jsx in $KIT" >&2; exit 1; }
TMP=$(mktemp -d); JSX="$TMP/run.jsx"; STATUS="$TMP/status.txt"
cat > "$JSX" <<JS
(function(){
  var out; var f=new File(${(qqq)STATUS}); f.lineFeed="Unix";
  try{
    var aep=${(qqq)AEP};
    if(aep){ var target=new File(aep); var p=app.project;
      if(p && p.dirty && (!p.file || p.file.fsName!=target.fsName)){ out="REFUSED: unsaved changes in "+(p.file?p.file.fsName:"(unsaved project)")+" - save it first"; f.open("w"); f.write(out); f.close(); return; }
      if(target.exists){ if(!p || !p.file || p.file.fsName!=target.fsName) app.open(target); } }
    PPS_KIT_ROOT=${(qqq)KIT};
    var bf=new File(${(qqq)KIT}+"/render-h264.jsx"); bf.encoding="UTF-8"; bf.open("r"); var src=bf.read(); bf.close();
    var res=eval(src);
    if(aep){ var sv=new File(aep); app.project.save(sv); res+="\nsaved "+sv.fsName; }
    out="OK\n"+res;
  }catch(e){ var m=""; try{ m=String(e.message||e); }catch(a){ m="(unprintable error)"; } try{ if(e.line) m+=" (line "+e.line+")"; }catch(b){} out="ERROR: "+m; }
  try{ PPS_KIT_ROOT=undefined; }catch(x){}
  f.open("w"); f.write(out); f.close();
})();
JS
osascript - "$JSX" <<APPLESCRIPT >/dev/null
on run argv
  set js to "var _f=new File(" & quoted form of (item 1 of argv) & "); _f.encoding='UTF-8'; _f.open('r'); var _s=_f.read(); _f.close(); eval(_s); 'ok';"
  with timeout of 1800 seconds
    tell application "$AE_APP"
      activate
      DoScript js
    end tell
  end timeout
end run
APPLESCRIPT
for _ in {1..1800}; do [[ -s "$STATUS" ]] && grep -qE '^(OK|ERROR|REFUSED)' "$STATUS" && break; sleep 1; done
RESULT=$(cat "$STATUS" 2>/dev/null || echo "TIMEOUT: After Effects never reported back (dialog open? scripts not allowed to write files?) — see $KIT/build-log.txt")
rm -rf "$TMP"
echo "$RESULT"
[[ "$RESULT" == OK* ]]
