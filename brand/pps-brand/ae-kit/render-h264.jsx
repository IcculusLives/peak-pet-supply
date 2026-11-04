// render-h264.jsx — queue PPS_Summit and render it (royce-claude 2026-10-20). ES3. Output → ae-kit/renders/.
(function(){
  var KIT=(typeof PPS_KIT_ROOT!=="undefined")?PPS_KIT_ROOT:new File($.fileName).parent.fsName;
  var out=[]; var proj=app.project; var comp=null;
  for(var i=1;i<=proj.numItems;i++){ var it=proj.item(i); if(it instanceof CompItem && it.name=="PPS_Summit"){ comp=it; break; } }
  if(!comp) throw new Error("no comp PPS_Summit in the open project");
  var dir=new Folder(KIT+"/renders"); if(!dir.exists) dir.create();
  var rq=proj.renderQueue; while(rq.numItems>0) rq.item(1).remove();
  var rqi=rq.items.add(comp); var om=rqi.outputModule(1);
  var tried=[], picked=null, ext="mov";
  var cands=[["H.264 - Match Render Settings - 15 Mbps","mp4"],["H.264 - Match Render Settings - 40 Mbps","mp4"],["H.264","mp4"],["Apple ProRes 422","mov"],["Lossless","mov"]];
  for(var c=0;c<cands.length;c++){ try{ om.applyTemplate(cands[c][0]); picked=cands[c][0]; ext=cands[c][1]; break; }catch(e){ tried.push(cands[c][0]); } }
  var tmpl=om.templates; var tl=[]; for(var t=0;t<tmpl.length;t++) tl.push(tmpl[t]);
  out.push("output templates: "+tl.join(" | "));
  out.push("using: "+(picked||"(default)")+(tried.length?"  (not found: "+tried.join(", ")+")":""));
  var f=new File(dir.fsName+"/PPS_Summit_pearl_v1.4."+ext); om.file=f;
  try{ rqi.setSetting("Quality","Best"); rqi.setSetting("Resolution","Full"); }catch(e){}
  var t0=new Date().getTime(); rq.render(); var dt=Math.round((new Date().getTime()-t0)/1000);
  var ok=f.exists; out.push((ok?"RENDERED ":"NO FILE ")+f.fsName+"  ("+dt+" s"+(ok?", "+Math.round(f.length/1048576*10)/10+" MB":"")+")");
  proj.save();
  return out.join("\n");
})();
