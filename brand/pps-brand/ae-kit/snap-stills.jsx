// snap-stills.jsx — save the project + PNG stills of PPS_Summit at key frames (royce-claude 2026-10-20). ES3.
(function(){
  var KIT=(typeof PPS_KIT_ROOT!=="undefined")?PPS_KIT_ROOT:new File($.fileName).parent.fsName;
  var out=[]; var proj=app.project; var comp=null;
  for(var i=1;i<=proj.numItems;i++){ var it=proj.item(i); if(it instanceof CompItem && it.name=="PPS_Summit"){ comp=it; break; } }
  if(!comp) throw new Error("no comp PPS_Summit in the open project");
  var aep=new File(KIT+"/PPS_Summit.aep"); proj.save(aep); out.push("saved "+aep.fsName);
  var dir=new Folder(KIT+"/renders/stills"); if(!dir.exists) dir.create();
  var FR=[0,25,40,54,63,73,100,122,126,131,135,149,161,177,200,216,230,250,281,303,334,348,361,380,407,420,434,446];
  for(var k=0;k<FR.length;k++){ var f=FR[k]; var t=f/comp.frameRate; var png=new File(dir.fsName+"/f"+("000"+f).slice(-3)+".png");
    try{ comp.saveFrameToPng(t,png); out.push("f"+f+" ok"); }catch(e){ out.push("f"+f+" FAIL "+(e.message||e)); } }
  return out.join("\n");
})();
