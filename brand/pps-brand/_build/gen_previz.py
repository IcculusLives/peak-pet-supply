"""PPS "Summit" intro previz — v1.5 (2026-10-20: jaw, tail wag, boa on the riff, early white arcs, 14.9 s; see ae-kit/PPS-MOTION-SPEC.md) · v1.1 (2026-09-16): Casey's audio placement baked in + vocal-driven effects.
Concept: navy ground. The three peaks rise out of the ground line on the bed's grid, the dog drops from above and LANDS on the summit
on the PPS 2.5 hit (squash, dust, shockwave, the mountain thuds), the gold box slams on jj, PEAK pops, PET SUPPLY wipes on, the lockup settles.
PPS_2 is the VOCAL clip (starts 5.89): five short syllables 6.13–7.20, a HELD NOTE 7.21–9.39 (the dog "howls": sound-wave arcs from the snout,
a gold aura that follows the real voice level, the dog swells), six punchy syllables 9.48–11.26 (arc bursts, PEAK bounces, box blinks),
then the 808 at 12.03 = final pulse + flash and the four FB-pearl ticks 12.19 / 12.50 / 13.39 / 13.68 = lock ticks on box / PEAK / PET SUPPLY / lockup. Still from 13.9.
Every number is a slider in the page; vocal cues are FILE-relative so they ride the PPS 2 start slider.
Serve the PACKAGE ROOT (launch.json → pps-previz :8767) and open /ae-kit/intro-previz.html — audio is referenced as ../audio/."""
import json, math, os, re, subprocess, tempfile
from lib import *
K=os.path.abspath(HERE+'../ae-kit')+'/'
reg=json.load(open(K+'parts/registration.json'))
FPS=30; END=447   # v1.5: 14.9 s — ~0.7 s of silence after the riff while the boa tail keeps swaying
fr=lambda t: int(math.floor(t*FPS+0.5))          # round-half-up = JS Math.round (Python round() is banker's)
# ---- audio slots: key, file, length, cue offsets inside the file (s), start, gain, label  — starts/gains = Casey's 📋 paste 2026-10-18 00:48 (v1.4 LOCK candidate; v1.2: dog lands on the 808; 2.5 and jj moved later; was 11.96 / 2.49 / 4.40 on 2026-09-16) ----
AUDIO=[('bed','PPS_1pearl.wav',14.58,[0.82,1.33,1.79,2.13,2.49,2.75,3.25,3.48,4.41,4.66,5.17,5.63,5.97,6.33,6.59,7.09,7.32,7.56,8.25,8.49,8.96,9.47,9.80,10.17],0.00,0.60,'bed (1pearl 14.6 s)'),
       ('k808','PPS_808wFB.wav',1.01,[0.075],2.28,0.92,'808 w/ FB (1.0 s)'),
       ('fb','PPS_FB_pearl.wav',2.60,[0.60,0.91,1.80,2.09],11.59,0.80,'FB pearl (2.6 s, 4 hits)'),
       ('two5','PPS_2.5.wav',1.11,[0.17],3.96,0.70,'PPS 2.5 (1.1 s hit)'),
       ('p2','PPS_2.wav',6.13,[0.24,0.48,0.68,1.12,1.31,3.59,3.95,4.34,4.73,5.08,5.37,6.12],5.89,0.55,'PPS 2 — VOCAL (6.1 s)'),
       ('jj','PPS_jj_short.wav',1.11,[0.17],4.88,0.80,'jj short (1.1 s hit)')]
# ---- vocal analysis of PPS_2.wav (250–3500 Hz RMS): syllable onsets, the held note, and the level curve every 0.1 s (dBFS) ----
VOC_SYL=[0.24,0.48,0.68,1.12,1.31,3.59,3.95,4.34,4.73,5.08,5.37,6.12]
FB_HITS=[0.20,0.52,0.83,1.12,1.44,1.74,2.02,2.33]; FB_STR=[0.89,0.28,0.38,1.0,0.28,0.53,0.73,0.25]   # v1.5: spectral-flux onsets inside PPS_FB_pearl.wav (s) + strength — the boa pulses on these
MOUTH25=[-37, -29, -21, -18, -17, -19, -20, -25, -24, -19, -22, -28, -28, -32, -33, -20, -16, -17, -20, -21, -21, -29, -36, -36, -36, -36, -37, -32, -28, -31, -36, -49, -49, -47]   # v1.5: 250–3500 Hz RMS (dBFS) per frame inside PPS_2.5.wav — drives the jaw for the "honey I said" stabs
MOUTH2=[-48, -48, -47, -47, -44, -40, -35, -25, -18, -18, -17, -18, -23, -27, -21, -19, -27, -29, -28, -34, -26, -17, -16, -18, -20, -21, -24, -34, -37, -35, -37, -36, -37, -29, -24, -25, -29, -36, -36, -27, -21, -18, -18, -18, -18, -18, -19, -18, -17, -16, -17, -18, -18, -17, -18, -18, -19, -19, -20, -21, -22, -22, -22, -23, -24, -23, -24, -24, -24, -23, -22, -22, -23, -23, -22, -22, -21, -21, -20, -21, -21, -22, -23, -21, -23, -23, -22, -22, -20, -21, -22, -22, -21, -21, -22, -23, -23, -23, -22, -24, -24, -23, -24, -25, -25, -26, -27, -26, -22, -19, -19, -20, -25, -28, -25, -26, -28, -29, -25, -20, -19, -19, -19, -22, -26, -27, -29, -30, -30, -28, -24, -19, -19, -19, -20, -24, -25, -27, -25, -26, -28, -30, -27, -22, -20, -20, -21, -28, -29, -31, -31, -31, -28, -25, -25, -27, -25, -25, -28, -36, -33, -27, -26, -28, -28, -30, -28, -29, -31, -33, -32, -34, -37, -32, -30, -37, -38, -42, -43, -45, -44, -45, -46, -45]   # same, inside PPS_2.wav
VOC_LEVEL=[-34,-49,-39,-20,-23,-21,-31,-22,-22,-34,-39,-35,-29,-34,-20,-21,-20,-20,-20,-22,-24,-25,-26,-26,-25,-24,-23,-24,-25,-25,-25,-23,-26,-26,-26,-30,-26,-22,-29,-32,-22,-22,-31,-31,-21,-25,-29,-34,-23,-28,-33,-29,-28,-37,-29,-32,-33,-36,-32,-43,-46,-49]
# ---- visual hits (absolute s). v1.2 2026-10-18: land 2.42 (808 hit 2.31), box 4.07 (2.5 hit 4.13), PEAK 4.99 (jj hit 5.05); flash 12.03 now rides the vocal's last note; ticks on the FB pearl. (v1.1 was land 2.60 / box 4.50 / peak 4.71) ----
HITS={'mtn_l':0.82,'mtn_c':1.33,'mtn_r':1.79,'land':2.42,'box':4.07,'peak':4.99,'pet':5.60,'settle':5.89,'flash':12.03,'still':13.90,
      'wave_n':2,'wave_amt':0.6,'wave1':6.33,'wave2':7.09,'wave3':8.25,'wave4':8.96,'wave5':9.80,'wave6':10.17,
      'voc_amt':1.0,'voc_from':1.32,'voc_to':6.13,'voc_rate':5,'voc_syl':1.0,'lock_amt':1.0,
      'syl2_off':-0.12,                                   # v1.3: shift (s) applied to the late syllable group (in-file >= 3.5 s) — Casey heard the final bursts late
      'duck_t':2.47,'duck_len':0.14,'duck_amt':1.0,        # v1.3: bed duck — cuts the bed's lone kick at 2.49–2.58 right after the 808 (near-silence either side)
      'boa_off':0.20,'boa_grow':2.13,'boa_size':1.0,'boa_sparkle':1.0,'boa_amt':0.8,'boa_tail':78,   # v1.5: boa grows from the riff's first hit (11.79) to its last (13.92), pulses on every hit; tail 78 px clears the summit
      'wag_amt':6.0,'jaw_amt':40.0}   # v1.3: pink sparkly boa grows round the neck when the FB pearl starts (boa_off = offset from a_fb)   # voc_from/to = window INSIDE the PPS 2 file (s); voc_rate = frames between howl arcs
GAIN={a[0]:a[5] for a in AUDIO}; START={a[0]:a[4] for a in AUDIO}
def table(h,st):   # mirrored line for line by computeF() in the page
    p2=st['p2']; fb=st['fb']
    return {'MTN_L':fr(h['mtn_l']),'MTN_C':fr(h['mtn_c']),'MTN_R':fr(h['mtn_r']),'DROP':fr(h['land'])-10,'LAND':fr(h['land']),'BOX':fr(h['box']),'PEAK':fr(h['peak']),'PET':fr(h['pet']),'SETTLE':fr(h['settle']),'FLASH':fr(h['flash']),'STILL':fr(h['still']),
            'WAVES':[fr(h[f'wave{i+1}']) for i in range(int(h['wave_n']))],
            'VOC0':fr(p2+h['voc_from']),'VOC1':fr(p2+h['voc_to']),'SYL':[fr(p2+s+(h['syl2_off'] if s>=3.5 else 0)) for s in VOC_SYL if h['voc_from']<=s<=h['voc_to'] and s<6.0],   # v1.5: the 6.12 burst is dropped
            'BOA':fr(fb+h['boa_off']),'DUCK':[fr(h['duck_t']),fr(h['duck_t']+h['duck_len'])],
            'LOCKS':[fr(fb+c) for c in AUDIO[2][3]]}
F=table(HITS,START)
json.dump({'fps':FPS,'frames':END,'audio':[{'key':a[0],'file':a[1],'len':a[2],'cues':a[3],'start':a[4],'gain':a[5]} for a in AUDIO],'hits':HITS,'vocal':{'syllables':VOC_SYL,'level_0.1s':VOC_LEVEL},'F':F},open(K+'parts/timeline.json','w'),indent=1)
def body(name):
    s=open(K+'parts/'+name).read(); return s[s.index('>',s.index('<svg'))+1:s.rindex('</svg>')]
lk=reg['lockup']; dg=reg['dog']; bx=reg['box']; pk=reg['peak']; ps=reg['pet-supply']; gy=reg['ground_y']; sm=reg['summit']; sn=reg['snout']
ml,mc,mr=reg['mountain-left'],reg['mountain-center'],reg['mountain-right']
aud_el=''.join(f'<audio id="au_{a[0]}" src="../audio/{a[1]}" preload="auto"></audio>' for a in AUDIO)
AJS=json.dumps([{'k':a[0],'file':a[1],'len':a[2],'cues':a[3],'label':a[6]} for a in AUDIO])
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Peak Pet Supply — "Summit" intro previz v1.1</title>
<style>
html,body{{margin:0;background:#111;color:#ddd;font:13px/1.4 -apple-system,Helvetica,sans-serif;height:100%}}
#stage{{position:relative;width:100vw;height:56.25vw;max-height:calc(100vh - 54px);max-width:calc((100vh - 54px)*1.7778);margin:0 auto;background:#000;overflow:hidden}}
svg{{width:100%;height:100%;display:block}}
#ui{{position:fixed;left:0;right:0;bottom:0;padding:10px 14px;background:rgba(0,0,0,.8);display:flex;gap:12px;align-items:center;z-index:6}}
#ui input[type=range]{{flex:1}} #ui button{{background:#222;color:#eee;border:1px solid #555;padding:4px 10px;border-radius:4px;cursor:pointer}}
.clean #ui,.clean #panel{{display:none}} #t{{font-variant-numeric:tabular-nums;min-width:150px}} #cue{{color:#F6C808;min-width:260px}} #vol{{width:90px}}
#panel{{position:fixed;top:10px;right:10px;width:340px;max-height:calc(100vh - 80px);overflow:auto;background:rgba(0,0,0,.85);border:1px solid #333;border-radius:8px;padding:10px 12px;display:none;z-index:5}} body.tune #panel{{display:block}}
#panel h4{{margin:10px 0 4px;color:#F6C808;font-size:12px;text-transform:uppercase;letter-spacing:.08em}}
#panel label{{display:grid;grid-template-columns:110px 1fr 56px;gap:8px;align-items:center;margin:4px 0;font-size:12px}} #panel output{{text-align:right;font-variant-numeric:tabular-nums;color:#F6C808}}
#panel button{{background:#222;color:#eee;border:1px solid #555;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:11px;margin-right:4px}}
#panel .derived{{color:#8aa;font-size:11px;margin:2px 0 6px}} #panel input[type=file]{{font-size:10px;width:100%;color:#888}}
@media (max-width:1100px){{ body{{overflow:auto}} #stage{{max-height:none}} body.tune #panel{{position:static;width:auto;max-height:none;margin:10px auto 72px;max-width:520px}} #ui{{flex-wrap:wrap}} }}
</style></head><body>
<div id="stage"><svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="wash" cx=".5" cy=".62" r=".6"><stop offset="0" stop-color="#10689A" stop-opacity=".28"/><stop offset="1" stop-color="#10689A" stop-opacity="0"/></radialGradient>
 <radialGradient id="flashG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F8F8F8" stop-opacity=".85"/><stop offset="1" stop-color="#F8F8F8" stop-opacity="0"/></radialGradient>
 <radialGradient id="thudG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F6C808" stop-opacity=".5"/><stop offset="1" stop-color="#F6C808" stop-opacity="0"/></radialGradient>
 <radialGradient id="auraG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F6C808" stop-opacity=".55"/><stop offset=".6" stop-color="#F6C808" stop-opacity=".12"/><stop offset="1" stop-color="#F6C808" stop-opacity="0"/></radialGradient>
 <clipPath id="clipPet"><rect id="cPet" x="{ps[0]-8}" y="{ps[1]-10}" width="0" height="{ps[3]-ps[1]+20}"/></clipPath>
 <clipPath id="clipGround"><rect x="0" y="0" width="1920" height="{gy}"/></clipPath>
 <mask id="mTailCut"><rect x="0" y="0" width="1920" height="1080" fill="white"/><polygon points="812,298 838,322 838,364 760,374 735,345 780,322" fill="black"/></mask>
 <clipPath id="cTail"><polygon points="806,290 844,318 838,364 760,374 735,345 780,322"/></clipPath>
</defs>
<rect width="1920" height="1080" fill="{NAVY}"/>
<rect id="wash" width="1920" height="1080" fill="url(#wash)" opacity="0"/>
<rect id="thud" width="1920" height="1080" fill="url(#thudG)" opacity="0"/>
<ellipse id="aura" cx="{sn[0]}" cy="{sn[1]}" rx="900" ry="620" fill="url(#auraG)" opacity="0"/>
<g id="lockup" transform-origin="{lk[4]} {lk[5]}">
 <g id="emblem" transform-origin="{sm[0]} {gy}">
  <g clip-path="url(#clipGround)">
   <g id="mtnL" transform-origin="{ml[4]} {gy}">{body('01-mountain-left.svg')}</g>
   <g id="mtnC" transform-origin="{mc[4]} {gy}">{body('02-mountain-center.svg')}</g>
   <g id="mtnR" transform-origin="{mr[4]} {gy}">{body('03-mountain-right.svg')}</g>
  </g>
  <g id="dust"></g>
  <g id="dog" transform-origin="{dg[4]} {dg[3]}"><g id="boaB"></g><g id="dogTail" clip-path="url(#cTail)" transform-origin="826 308">{body('05-dog.svg')}</g><g mask="url(#mTailCut)">{body('05-dog.svg')}</g><g id="jaw" transform-origin="1042 158"><polygon points="1042,158 1067,150.5 1067,146 1061,143.5 1046,151" fill="{OFFWHITE}"/></g><g id="boaF"></g></g>
 </g>
 <g id="box" transform-origin="{bx[4]} {bx[5]}">{body('06-box-gold.svg')}</g>
 <g id="peak" transform-origin="{pk[4]} {pk[5]}">{body('07-peak.svg')}</g>
 <g id="pet" transform-origin="{ps[4]} {ps[5]}"><g clip-path="url(#clipPet)">{body('08-pet-supply.svg')}</g></g>
</g>
<g id="arcs"></g>
<g id="rings"></g>
<rect id="flash" width="1920" height="1080" fill="url(#flashG)" opacity="0"/>
</svg></div>
<div id="panel"></div>
<div id="ui"><button id="play">▶ Play with audio</button><button id="replay">↺</button><input id="scrub" type="range" min="0" max="{END-1}" value="0"><span id="t"></span><span id="cue"></span><label>master <input id="vol" type="range" min="0" max="1" step=".01" value="1"></label><button id="tog">⚙︎ tune</button></div>
{aud_el}
<script>
const FPS={FPS},END={END};
const AUDIO={AJS};
const VOC_SYL={json.dumps(VOC_SYL)}, VOC_LEVEL={json.dumps(VOC_LEVEL)}, MOUTH25={json.dumps(MOUTH25)}, MOUTH2={json.dumps(MOUTH2)}, FB_HITS={json.dumps(FB_HITS)}, FB_STR={json.dumps(FB_STR)};   // PPS 2 analysis (file-relative): syllable onsets, level every 0.1 s
const SN=[{sn[0]},{sn[1]}];   // the dog's snout — where the voice comes from
// ---- tunables: defaults baked by _build/gen_previz.py (v1.1 = Casey's audio placement); the panel edits them live; 📋 copies CFG back for baking ----
const DEFAULTS={{{','.join(f'a_{k}:{v}' for k,v in START.items())},{','.join(f'g_{k}:{v}' for k,v in GAIN.items())},{','.join(f'{k}:{v}' for k,v in HITS.items())}}};
let CFG=Object.assign({{}},DEFAULTS); try{{ Object.assign(CFG,JSON.parse(localStorage.getItem('pps_summit_cfg15')||'{{}}')); }}catch(e){{}}
const $=id=>document.getElementById(id), fr=t=>Math.round(t*FPS), s2=t=>(+t).toFixed(2);
let F={{}}, CUES=[];
function computeF(){{ const c=CFG, p2=c.a_p2, fb=c.a_fb;   // mirror of the Python table() — keep the two in sync
  F={{MTN_L:fr(c.mtn_l),MTN_C:fr(c.mtn_c),MTN_R:fr(c.mtn_r),DROP:fr(c.land)-10,LAND:fr(c.land),BOX:fr(c.box),PEAK:fr(c.peak),PET:fr(c.pet),SETTLE:fr(c.settle),FLASH:fr(c.flash),STILL:fr(c.still),
     WAVES:Array.from({{length:Math.round(c.wave_n)}},(_,i)=>fr(c['wave'+(i+1)])),
     VOC0:fr(p2+c.voc_from),VOC1:fr(p2+c.voc_to),SYL:VOC_SYL.filter(s=>s>=c.voc_from&&s<=c.voc_to&&s<6.0).map(s=>fr(p2+s+(s>=3.5?c.syl2_off:0))),
     BOA:fr(fb+c.boa_off),DUCK:[fr(c.duck_t),fr(c.duck_t+c.duck_len)],
     LOCKS:AUDIO[2].cues.map(x=>fr(fb+x))}};
  CUES=[[0,'start'],[F.MTN_L,'left peak rises ('+s2(c.mtn_l)+')'],[F.MTN_C,'summit rises ('+s2(c.mtn_c)+')'],[F.MTN_R,'right peak rises ('+s2(c.mtn_r)+')'],[F.DROP,'dog drops in'],[F.LAND,'LANDING ('+s2(c.land)+') — squash, dust, shockwave, thud'],
    [F.BOX,'gold box slams ('+s2(c.box)+')'],[F.PEAK,'PEAK pops ('+s2(c.peak)+')'],[F.PET,'PET SUPPLY wipes on ('+s2(c.pet)+')'],[F.SETTLE,'lockup settles ('+s2(c.settle)+') — breathe'],
    [F.VOC0,'VOCAL window opens ('+s2(p2+c.voc_from)+') — howl arcs + aura follow the voice'],[F.VOC1,'vocal window closes ('+s2(p2+c.voc_to)+')'],
    [F.FLASH,'final pulse + flash ('+s2(c.flash)+')'],[F.STILL,'dead still — hold'],[F.BOA,'BOA grows round the neck ('+s2(fb+c.boa_off)+') — pink, sparkly, venom-style'],[F.DUCK[0],'bed ducked ('+s2(c.duck_t)+'–'+s2(c.duck_t+c.duck_len)+') — kick removed'],
    ...F.WAVES.map((w,i)=>[w,'SHOCKWAVE '+(i+1)+' ('+s2(c['wave'+(i+1)])+')']),...F.SYL.map((s,i)=>[s,'syllable '+(i+1)+' ('+s2(s/FPS)+') — burst, PEAK bounce, box blink']),
    ...F.LOCKS.map((l,i)=>[l,'lock tick '+(i+1)+' ('+s2(l/FPS)+'): '+['box','PEAK','PET SUPPLY','whole lockup'][i]])].sort((a,b)=>a[0]-b[0]);
  const d=$('derived'); if(d) d.innerHTML=AUDIO.map(a=>`<div class="derived"><b>${{a.label}}</b> hits at ${{a.cues.slice(0,8).map(x=>s2(CFG['a_'+a.k]+x)).join(' · ')}}${{a.cues.length>8?' …':''}}</div>`).join('')+`<div class="derived"><b>vocal effects</b> ${{s2(p2+c.voc_from)}} → ${{s2(p2+c.voc_to)}} s · ${{F.SYL.length}} syllables inside · lock ticks ${{F.LOCKS.map(l=>s2(l/FPS)).join(' · ')}}</div>`; }}
// ---- tuning panel ----
const SL_A=AUDIO.map(a=>['a_'+a.k,a.label+' start',0,14.5,0.01,'s']), SL_G=AUDIO.map(a=>['g_'+a.k,a.label.split(' (')[0]+' vol',0,1,0.01,'']);
const SL_H=[['mtn_l','left peak',0,6,0.01,'s'],['mtn_c','summit',0,6,0.01,'s'],['mtn_r','right peak',0,6,0.01,'s'],['land','dog LANDS',0.5,8,0.01,'s'],['box','box slam',1,10,0.01,'s'],['peak','PEAK pop',1,10,0.01,'s'],['pet','PET SUPPLY',1,10,0.01,'s'],['settle','settle',1,11,0.01,'s'],['flash','final flash',8,14.4,0.01,'s'],['still','dead still',8,14.5,0.01,'s']];
const SL_W=[['wave_n','shockwaves (count)',0,6,1,''],['wave_amt','shockwave strength',0,1.5,0.05,'×'],...[1,2,3,4,5,6].map(i=>['wave'+i,'shockwave '+i,0,14.4,0.01,'s'])];
const SL_V=[['jaw_amt','jaw opens (deg)',0,60,1,'°'],['wag_amt','tail wag (deg)',0,15,0.5,'°'],['voc_amt','vocal strength',0,2,0.05,'×'],['voc_from','window from (in file)',0,6.13,0.01,'s'],['voc_to','window to (in file)',0,6.13,0.01,'s'],['voc_rate','howl arc every',2,12,1,'f'],['voc_syl','syllable punch',0,2,0.05,'×'],['syl2_off','late syllables shift',-0.5,0.5,0.01,'s'],['lock_amt','end lock ticks',0,2,0.05,'×']];
const SL_D=[['duck_t','bed duck start',0,14,0.01,'s'],['duck_len','bed duck length',0,1,0.01,'s'],['duck_amt','bed duck depth',0,1,0.05,'×']];
const SL_B=[['boa_off','boa start (from FB pearl)',-2,2,0.01,'s'],['boa_grow','boa grow time',0.3,3,0.05,'s'],['boa_size','boa size',0.6,1.8,0.05,'×'],['boa_sparkle','boa sparkle',0,2,0.05,'×'],['boa_tail','boa tail length',0,400,5,'px'],['boa_amt','boa presence',0,1,0.05,'×']];
const ALL=[...SL_A,...SL_G,...SL_H,...SL_W,...SL_V,...SL_D,...SL_B];
function row([k,l,a,b,st,u]){{ return `<label><span>${{l}}</span><input type="range" data-k="${{k}}" min="${{a}}" max="${{b}}" step="${{st}}" value="${{CFG[k]}}"><output>${{s2(CFG[k])}}${{u}}</output></label>`; }}
function buildPanel(){{ const pn=$('panel');
  pn.innerHTML='<b>tune</b> <button id="pReset">reset</button> <button id="pCopy">📋 copy settings</button>'
   +'<h4>audio starts</h4>'+SL_A.map(row).join('')+'<div id="derived"></div>'
   +'<h4>bed duck (kick removal)</h4>'+SL_D.map(row).join('')
   +'<h4>vocal effects (ride the PPS 2 start)</h4>'+SL_V.map(row).join('')
   +'<h4>boa (rides the FB pearl start)</h4>'+SL_B.map(row).join('')
   +'<h4>hits</h4>'+SL_H.map(row).join('')+'<h4>extra shockwaves</h4>'+SL_W.map(row).join('')
   +'<h4>gains</h4>'+SL_G.map(row).join('')
   +'<h4>swap a file</h4>'+AUDIO.map(a=>`<label><span>${{a.label.split(' (')[0]}}</span><input type="file" accept="audio/*" data-k="${{a.k}}"></label>`).join('');
  pn.querySelectorAll('input[type=range]').forEach(r=>{{ r.oninput=()=>{{ CFG[r.dataset.k]=+r.value; r.nextElementSibling.textContent=s2(r.value)+(ALL.find(x=>x[0]===r.dataset.k)[5]); try{{localStorage.setItem('pps_summit_cfg15',JSON.stringify(CFG));}}catch(e){{}} computeF(); setVol(); if(playing) rescheduleCues(); render(+sc.value); }}; }});
  pn.querySelectorAll('input[type=file]').forEach(i=>{{ i.onchange=()=>{{ const f=i.files[0]; if(!f) return; const el=$('au_'+i.dataset.k); el.src=URL.createObjectURL(f); el.onloadedmetadata=()=>{{ const a=AUDIO.find(x=>x.k===i.dataset.k); a.len=el.duration; a.file=f.name; }}; }}; }});
  $('pReset').onclick=()=>{{ CFG=Object.assign({{}},DEFAULTS); try{{localStorage.removeItem('pps_summit_cfg15');}}catch(e){{}} buildPanel(); setVol(); render(+sc.value); }};
  $('pCopy').onclick=()=>{{ const txt=JSON.stringify(CFG); (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>{{$('pCopy').textContent='✓ copied — paste to Claude';}},()=>{{prompt('copy these settings:',txt);}}); setTimeout(()=>$('pCopy').textContent='📋 copy settings',2500); }};
  computeF(); }}
// ---- easing ----
const eo=t=>1-Math.pow(1-t,3), ei=t=>t*t*t, eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2, cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), U=(f,a,b)=>cl((f-a)/(b-a));
const pop=(f,f0,len=12,over=1.18)=>{{ if(f<f0) return 0; const u=U(f,f0,f0+len); return u<.45? over*eo(u/.45) : over-(over-1)*eio((u-.45)/.55); }};
const rise=(f,f0,len=16,over=1.05)=>{{ if(f<f0) return 0; const u=U(f,f0,f0+len); return u<.6? over*eo(u/.6) : over-(over-1)*eio((u-.6)/.4); }};
const pulse=(f,f0,len,amt)=>{{ if(f<f0||f>f0+len) return 1; const u=U(f,f0,f0+len); return u<.35?1+amt*eo(u/.35):1+amt*(1-eio((u-.35)/.65)); }};
// voice level 0..1 at frame f (from the PPS 2 envelope, −40 dB → 0, −18 dB → 1), only inside the vocal window
function vlevel(f){{ if(f<F.VOC0||f>F.VOC1) return 0; const tf=f/FPS-CFG.a_p2; const i=tf*10, i0=Math.floor(i), i1=Math.min(VOC_LEVEL.length-1,i0+1); if(i0<0||i0>=VOC_LEVEL.length) return 0; const db=VOC_LEVEL[i0]+(VOC_LEVEL[i1]-VOC_LEVEL[i0])*(i-i0); return cl((db+40)/22); }}
// v1.5: jaw / early-arc level — 250–3500 Hz RMS of the three vocal placements (PPS 2.5, jj = the same stab, PPS 2), fast attack, ~4-frame release
function mouthRaw(f){{ let v=0; for(const [arr,k] of [[MOUTH25,'a_two5'],[MOUTH25,'a_jj'],[MOUTH2,'a_p2']]){{ const i=f-fr(CFG[k]); if(i>=0&&i<arr.length) v=Math.max(v,cl((arr[i]+34)/16)); }} return v; }}
function mouth(f){{ let v=0; for(let k=0;k<4;k++) v=Math.max(v,mouthRaw(f-k)*Math.pow(0.72,k)); return v>0.06?v:0; }}
function rings(f){{ let s='';
  const ring=(f0,cx,cy,r0,r1,w0,o0,len,col='{GOLD}')=>{{ if(f<f0||f>f0+len)return; const u=eo(U(f,f0,f0+len)); s+=`<circle cx="${{cx}}" cy="${{cy}}" r="${{r0+(r1-r0)*u}}" fill="none" stroke="${{col}}" stroke-width="${{w0*(1-u)+1}}" opacity="${{o0*(1-u)}}"/>`; }};
  ring(F.LAND,{sm[0]},{sm[1]},40,1300,44,.8,30,'{OFFWHITE}'); ring(F.LAND+3,{sm[0]},{sm[1]},30,800,20,.5,24);
  for(const w of F.WAVES){{ const a=CFG.wave_amt; ring(w,{sm[0]},{sm[1]},40,900*a+200,30*a,.7,26,'{OFFWHITE}'); ring(w+3,{sm[0]},{sm[1]},30,600*a+120,14*a,.45,22); }}
  ring(F.BOX,{bx[4]},{bx[5]},80,700,14,.6,20); ring(F.PEAK,{pk[4]},{pk[5]},30,420,10,.5,18,'{OFFWHITE}'); ring(F.SETTLE,{lk[4]},{lk[5]},120,900,10,.4,22);
  ring(F.FLASH,{lk[4]},{lk[5]},200,1500,40,.7,40,'{OFFWHITE}'); ring(F.FLASH+4,{lk[4]},{lk[5]},200,1100,24,.4,34);
  const LC=[[{bx[4]},{bx[5]}],[{pk[4]},{pk[5]}],[{ps[4]},{ps[5]}],[{lk[4]},{lk[5]}]]; F.LOCKS.forEach((l,i)=>{{ const a=CFG.lock_amt; ring(l,LC[i][0],LC[i][1],20,(i==3?900:420)*a+60,10*a,.6,18); }});
  $('rings').innerHTML=s; }}
// sound-wave arcs from the snout: a steady stream while the voice is on (spaced voc_rate frames, sized by the live level) + a 3-arc burst on every syllable
function arcs(f){{ let s=''; const a=CFG.voc_amt, E0=fr(Math.min(CFG.a_two5,CFG.a_jj,CFG.a_p2)); if(a<=0||f<E0||f>F.VOC1+24){{ $('arcs').innerHTML=''; return; }}
  const arc=(age,len,r0,spd,w,o,col='{OFFWHITE}',tilt=-18)=>{{ if(age<0||age>len) return; const u=age/len, r=r0+spd*age*(1-0.35*u); const a0=(tilt-32)*Math.PI/180, a1=(tilt+32)*Math.PI/180;
    s+=`<path d="M${{SN[0]+r*Math.cos(a0)}},${{SN[1]+r*Math.sin(a0)}} A${{r}},${{r}} 0 0 1 ${{SN[0]+r*Math.cos(a1)}},${{SN[1]+r*Math.sin(a1)}}" fill="none" stroke="${{col}}" stroke-width="${{w*(1-u)+1}}" stroke-linecap="round" opacity="${{o*(1-u)}}"/>`; }};
  const rate=Math.max(2,Math.round(CFG.voc_rate));
  for(let s0=E0; s0<Math.min(f+1,F.VOC0); s0+=rate){{ const lv=mouth(s0)*0.9; if(lv<0.12) continue; arc(f-s0,22,28,14+10*lv,5*a*lv+1,0.55*a*lv); }}   /* v1.5: white arcs on the "honey I said" phrases */
  for(let s0=F.VOC0; s0<=Math.min(f,F.VOC1-15); s0+=rate){{ const lv=vlevel(s0); if(lv<0.12) continue; arc(f-s0,22,28,14+10*lv,5*a*lv+1,0.55*a*lv); }}
  for(const sy of F.SYL){{ const b=CFG.voc_syl*a; for(let k=0;k<3;k++) arc(f-sy-k*2,20,34+k*26,22,8*b,0.9*b,k==1?'{GOLD}':'{OFFWHITE}'); }}
  $('arcs').innerHTML=s; }}
// ---- the boa (v1.3): a pink, sparkly feather boa grows round the dog's neck when the FB pearl starts — venom-style, two tendrils from the back of the neck wrap round and meet under the chin; then it breathes with the voice and sways ----
const NECK={{cx:1006,cy:190,rx:43,ry:15,tilt:24*Math.PI/180}};   // comp px, read off 05-dog.svg (back of neck ≈ 962,178 · throat ≈ 1042,212)
const PINKS=['#FF3D9A','#FF6FB5','#FF8FC8','#FFB3DA','#F0197F'];
const h1=i=>{{ const x=Math.sin(i*12.9898+78.233)*43758.5453; return x-Math.floor(x); }};   // deterministic 0..1 per tuft — no flicker
function boa(f){{ const bb=$('boaB'), bf=$('boaF'); const amt=CFG.boa_amt; if(amt<=0||f<F.BOA){{ bb.innerHTML=''; bf.innerHTML=''; return; }}
  const u=eo(U(f,F.BOA,F.BOA+Math.max(1,Math.round(CFG.boa_grow*FPS)))), age=(f-F.BOA)/FPS;
  let bp=0; for(let i=0;i<FB_HITS.length;i++){{ const d=f/FPS-(CFG.a_fb+FB_HITS[i]); if(d>=0) bp+=(0.04+0.07*FB_STR[i])*Math.exp(-d*10); }}   /* v1.5: the collar pulses on every riff hit */
  const lv=vlevel(f), size=CFG.boa_size*(1+0.06*lv*CFG.voc_amt+bp), sway=u>=1?Math.sin(f/FPS*2*Math.PI/1.7)*2.5*Math.PI/180:0;
  const N=NECK, ct=Math.cos(N.tilt+sway), st=Math.sin(N.tilt+sway);
  const P=phi=>{{ const x=N.rx*size*Math.cos(phi), y=N.ry*size*Math.sin(phi); return [N.cx+x*ct-y*st, N.cy+x*st+y*ct]; }};
  let back='', front='', spark=''; const span=Math.PI*u, tufts=Math.max(1,Math.round(span/0.13));
  for(let k=0;k<=tufts;k++){{ const d=(k/tufts)*span;
    for(const dir of [1,-1]){{ const phi=Math.PI+dir*d, i=dir>0?k:tufts*2+5-k; let [x,y]=P(phi); const nz=h1(i), nz2=h1(i+97);
      const tip=u<1?cl(1-(span-d)/0.5):0; const wig=tip*Math.sin(age*14+i)*7*size; x+=-wig*st; y+=wig*ct;   // the growing tips wriggle
      const r=(10+5*nz)*size*(1-0.55*tip)+1, col=PINKS[i%PINKS.length];   // same gauge as the tail
      let c=`<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{(r*1.7).toFixed(1)}}" fill="${{col}}" opacity="${{(0.22*amt).toFixed(2)}}"/><circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{(r*1.25).toFixed(1)}}" fill="${{col}}" opacity="${{(0.45*amt).toFixed(2)}}"/><circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{r.toFixed(1)}}" fill="${{col}}" opacity="${{(0.95*amt).toFixed(2)}}"/>`;   // soft fluff halo + core = feathery
      if(nz2>0.55) c+=`<circle cx="${{(x+r*0.35*(nz2-0.5)).toFixed(1)}}" cy="${{(y-r*0.3).toFixed(1)}}" r="${{(r*0.42).toFixed(1)}}" fill="#FFD6EC" opacity="${{(0.55*amt).toFixed(2)}}"/>`;
      if(Math.sin(phi)>0) front+=c; else back+=c;   // lower half of the ellipse sits in front of the dog
      if(nz>0.62&&CFG.boa_sparkle>0){{ const tw=Math.pow(Math.max(0,Math.sin(f*0.33+nz*6.28)),4)*CFG.boa_sparkle*amt;
        if(tw>0.02){{ const s=(5+6*nz)*size*tw, sx=x+(nz2-0.5)*2*r, sy=y+(nz-0.5)*2*r; spark+=`<path d="M${{sx.toFixed(1)}},${{(sy-s).toFixed(1)}} Q${{sx.toFixed(1)}},${{sy.toFixed(1)}} ${{(sx+s).toFixed(1)}},${{sy.toFixed(1)}} Q${{sx.toFixed(1)}},${{sy.toFixed(1)}} ${{sx.toFixed(1)}},${{(sy+s).toFixed(1)}} Q${{sx.toFixed(1)}},${{sy.toFixed(1)}} ${{(sx-s).toFixed(1)}},${{sy.toFixed(1)}} Q${{sx.toFixed(1)}},${{sy.toFixed(1)}} ${{sx.toFixed(1)}},${{(sy-s).toFixed(1)}}Z" fill="#FFFFFF" opacity="${{tw.toFixed(2)}}"/>`; }}
        if(u>=1){{ const fl=(f*0.02+nz)%1, fo=(1-fl)*0.7*CFG.boa_sparkle*amt; if(fo>0.03) spark+=`<circle cx="${{(x+Math.sin(fl*9+i)*10).toFixed(1)}}" cy="${{(y-60*fl).toFixed(1)}}" r="${{(2.2*size).toFixed(1)}}" fill="#FFE3F2" opacity="${{fo.toFixed(2)}}"/>`; }} }}
    }} }}
  // the tail (v1.3b): once the two tendrils have met under the chin a strand drops from the meeting point, tapering to a little pompom, and swings like a pendulum with the sway
  if(CFG.boa_tail>0&&f>=F.BOA+Math.round(CFG.boa_grow*FPS*0.43)){{ const g0=F.BOA+Math.round(CFG.boa_grow*FPS*0.43), v=U(f,g0,g0+20), /* v1.5: tail drops on the riff's big 4th hit (12.71) */ vv=v<.7?1.12*eo(v/.7):1.12-0.12*eio((v-.7)/.3);   // drops with a little overshoot
    const L=CFG.boa_tail*size*vv, [bx0,by0]=P(0), th=sway*1.6+Math.sin(f/FPS*2*Math.PI/1.3+0.8)*7*Math.PI/180*(u>=1?1:0), n=Math.max(2,Math.round(L/8));
    for(let k=1;k<=n;k++){{ const q=k/n, nz=h1(900+k), nz2=h1(997+k); const bend=Math.sin(f/FPS*2*Math.PI/1.3)*0.18*q*q;   // lower end lags the swing
      const x=bx0+L*q*Math.sin(th+bend)+ (nz-0.5)*3, y=by0+L*q*Math.cos(th+bend); const r=((10+5*nz)*(1-0.35*q)+(k==n?10:0))*size, col=PINKS[(k+2)%PINKS.length];
      front+=`<circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{(r*1.7).toFixed(1)}}" fill="${{col}}" opacity="${{(0.22*amt).toFixed(2)}}"/><circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{(r*1.25).toFixed(1)}}" fill="${{col}}" opacity="${{(0.45*amt).toFixed(2)}}"/><circle cx="${{x.toFixed(1)}}" cy="${{y.toFixed(1)}}" r="${{r.toFixed(1)}}" fill="${{col}}" opacity="${{(0.95*amt).toFixed(2)}}"/>`;
      if(nz2>0.6&&CFG.boa_sparkle>0){{ const tw=Math.pow(Math.max(0,Math.sin(f*0.29+nz2*6.28)),4)*CFG.boa_sparkle*amt; if(tw>0.02){{ const sp=(4+5*nz2)*size*tw; spark+=`<path d="M${{x.toFixed(1)}},${{(y-sp).toFixed(1)}} Q${{x.toFixed(1)}},${{y.toFixed(1)}} ${{(x+sp).toFixed(1)}},${{y.toFixed(1)}} Q${{x.toFixed(1)}},${{y.toFixed(1)}} ${{x.toFixed(1)}},${{(y+sp).toFixed(1)}} Q${{x.toFixed(1)}},${{y.toFixed(1)}} ${{(x-sp).toFixed(1)}},${{y.toFixed(1)}} Q${{x.toFixed(1)}},${{y.toFixed(1)}} ${{x.toFixed(1)}},${{(y-sp).toFixed(1)}}Z" fill="#FFFFFF" opacity="${{tw.toFixed(2)}}"/>`; }} }} }} }}
  bb.innerHTML=back; bf.innerHTML=front+spark; }}
function dust(f){{ let s=''; if(f>=F.LAND && f<F.LAND+18){{ const u=U(f,F.LAND,F.LAND+18), e=eo(u);
  for(const [dx,dir] of [[-70,-1],[70,1]]) s+=`<ellipse cx="${{{dg[4]}+dx+dir*160*e}}" cy="${{{dg[3]}-6-30*e}}" rx="${{30+150*e}}" ry="${{12+34*e}}" fill="{OFFWHITE}" opacity="${{0.45*(1-u)}}"/>`; }} $('dust').innerHTML=s; }}
function render(f){{
  $('wash').setAttribute('opacity',(0.5*eo(U(f,0,40))).toFixed(3));
  const lv=vlevel(f), va=CFG.voc_amt;
  let syl=0; for(const sy of F.SYL) if(f>=sy&&f<sy+9) syl=Math.max(syl,1-eo(U(f,sy,sy+9)));   // 0..1 punch envelope of the nearest syllable
  syl*=CFG.voc_syl;
  // peaks rise out of the ground line (scale-Y about ground, tiny overshoot)
  for(const [id,f0] of [['mtnL',F.MTN_L],['mtnC',F.MTN_C],['mtnR',F.MTN_R]]) $(id).setAttribute('transform',`scale(1,${{Math.max(0.001,rise(f,f0)).toFixed(4)}})`);
  // the dog drops in (gravity ease-in), lands with a squash, recovers with a small overshoot; while singing it swells with the voice
  let dy=0, sy=1, sx=1, dop=1;
  if(f<F.DROP) dop=0; else if(f<F.LAND){{ dy=-760*(1-ei(U(f,F.DROP,F.LAND))); sy=1.06; sx=0.96; }}
  else {{ const u=U(f,F.LAND,F.LAND+10); sy=u<.3?1-0.16*eo(u/.3):0.84+0.16*(u<.7?eo((u-.3)/.4)*1.05:1.05-0.05*eio((u-.7)/.3)); sx=2-sy; }}
  sy*=1+0.045*va*lv+0.03*syl*va; sx*=1+0.015*va*lv;
  $('dog').setAttribute('opacity',dop); $('dog').setAttribute('transform',`translate(0,${{dy.toFixed(1)}}) scale(${{sx.toFixed(4)}},${{sy.toFixed(4)}})`);
  // v1.5: the jaw opens with the voice (lower jaw hinged at the mouth corner, hidden inside the muzzle when shut); the tail wags on the bed's pulse (0.785 s ≈ 76 BPM, hits at 0.575 + k·0.785) from the landing
  $('jaw').setAttribute('transform',`rotate(${{(CFG.jaw_amt*mouth(f)).toFixed(2)}})`);
  $('dogTail').setAttribute('transform',`rotate(${{(f>=F.LAND?CFG.wag_amt*Math.sin(2*Math.PI*(f/FPS-0.575)/0.785):0).toFixed(2)}})`);
  // landing: the whole emblem thuds about the ground line, gold wash blinks; extra shockwaves are smaller siblings
  let ex=pulse(f,F.LAND,14,0.035), ey=pulse(f,F.LAND,14,-0.05), th=f>=F.LAND?0.7*(1-eo(U(f,F.LAND,F.LAND+16))):0;
  for(const w of F.WAVES){{ const a=CFG.wave_amt; ex*=pulse(f,w,12,0.03*a); ey*=pulse(f,w,12,-0.04*a); if(f>=w) th=Math.max(th,0.5*a*(1-eo(U(f,w,w+14)))); }}
  th=Math.max(th,0.35*syl*va);   // box/ground blink on every syllable
  $('emblem').setAttribute('transform',`scale(${{ex.toFixed(4)}},${{ey.toFixed(4)}})`);
  $('thud').setAttribute('opacity',th.toFixed(3));
  // vocal aura: gold glow around the snout that follows the real voice level
  $('aura').setAttribute('opacity',(0.9*va*lv*lv).toFixed(3)); $('aura').setAttribute('rx',(700+400*lv).toFixed(0)); $('aura').setAttribute('ry',(480+280*lv).toFixed(0));
  // box slam, PEAK pop, PET SUPPLY wipe (+ syllable bounces and the end lock ticks)
  const la=CFG.lock_amt, L=F.LOCKS;
  const bs=pop(f,F.BOX,9,1.22)*(1+0.02*syl*va)*pulse(f,L[0],10,0.04*la); $('box').setAttribute('transform',`scale(${{bs.toFixed(4)}})`); $('box').setAttribute('opacity',f<F.BOX?0:1);
  const pks=pop(f,F.PEAK,11,1.3)*(1+0.07*syl*va)*pulse(f,L[1],10,0.06*la); $('peak').setAttribute('transform',`scale(${{pks.toFixed(4)}})`); $('peak').setAttribute('opacity',f<F.PEAK?0:Math.min(1,U(f,F.PEAK,F.PEAK+3)));
  $('cPet').setAttribute('width',({ps[2]-ps[0]+16}*eo(U(f,F.PET,F.PET+10))).toFixed(1)); $('pet').setAttribute('transform',`scale(${{(pulse(f,L[2],10,0.06*la)).toFixed(4)}})`);
  // settle + breathe (+ a slow swell with the held note), final pulse on the 808, last lock tick, still
  let s=pulse(f,F.SETTLE,12,0.03)*pulse(f,F.FLASH,16,0.045)*pulse(f,L[3],12,0.03*la);
  if(f>=F.SETTLE+12 && f<F.FLASH) s*=1+0.004*Math.sin((f-F.SETTLE-12)/FPS*2*Math.PI/2.4)+0.012*va*lv;
  $('lockup').setAttribute('transform',`scale(${{s.toFixed(4)}})`);
  $('flash').setAttribute('opacity',f>=F.FLASH?(0.55*(1-eo(U(f,F.FLASH,F.FLASH+20)))).toFixed(3):0);
  rings(f); dust(f); arcs(f); boa(f);
  $('t').textContent=`f ${{f}} · ${{(f/FPS).toFixed(2)}} s / ${{(END/FPS).toFixed(2)}}`; let c=''; for(const [cf,tx] of CUES) if(f>=cf) c=tx; $('cue').textContent=c;
}}
// ---- transport: wall clock is the master; every track (bed included) is scheduled off its own start slider ----
const sc=$('scrub'); let playing=false, raf, t0=0, wall=0, timers=[];
const A={{}}; AUDIO.forEach(a=>A[a.k]=$('au_'+a.k));
function setVol(){{ const m=+$('vol').value; AUDIO.forEach(a=>A[a.k].volume=cl(CFG['g_'+a.k]*m)); }} $('vol').oninput=setVol;
$('tog').onclick=()=>document.body.classList.toggle('tune');
sc.oninput=()=>{{ if(playing) stop(); render(+sc.value); }};
function now(){{ return t0+(performance.now()-wall)/1000; }}
function duck(t){{ const m=+$('vol').value, w=t>=CFG.duck_t&&t<CFG.duck_t+CFG.duck_len; A.bed.volume=cl(CFG.g_bed*m*(w?1-CFG.duck_amt:1)); }}   // v1.3: removes the bed's kick after the 808
function tick(){{ const t=now(); duck(t); const f=Math.min(END-1,Math.floor(t*FPS)); sc.value=f; render(f); if(f>=END-1){{ stop(); return; }} raf=requestAnimationFrame(tick); }}
function stop(){{ playing=false; cancelAnimationFrame(raf); timers.forEach(clearTimeout); timers=[]; AUDIO.forEach(a=>A[a.k].pause()); $('play').textContent='▶ Play with audio'; }}
function cue(el,start,len,t){{ if(t>=start && t<start+len){{ el.currentTime=t-start; el.play().catch(()=>{{}}); }} else if(t<start){{ el.currentTime=0; timers.push(setTimeout(()=>{{ if(playing) el.play().catch(()=>{{}}); }},(start-t)*1000)); }} }}
function rescheduleCues(){{ timers.forEach(clearTimeout); timers=[]; const t=now(); AUDIO.forEach(a=>{{ const st=CFG['a_'+a.k]; if(t<st){{ A[a.k].pause(); A[a.k].currentTime=0; timers.push(setTimeout(()=>{{ if(playing) A[a.k].play().catch(()=>{{}}); }},(st-t)*1000)); }} }}); }}
function play(from){{ if(playing) stop(); playing=true; $('play').textContent='■ Stop'; setVol(); t0=from/FPS; wall=performance.now(); AUDIO.forEach(a=>cue(A[a.k],CFG['a_'+a.k],a.len,t0)); tick(); }}
$('play').onclick=()=>{{ if(playing) stop(); else play(+sc.value); }}; $('replay').onclick=()=>play(0);
buildPanel(); setVol();
const q=new URLSearchParams(location.search); if(q.get('tune')) document.body.classList.add('tune'); if(q.get('clean')) document.body.classList.add('clean'); if(q.get('p')) sc.value=Math.round(+q.get('p')*(END-1)); if(q.get('f')) sc.value=+q.get('f'); render(+sc.value);
</script></body></html>'''
html=html.replace('</body>',open(HERE+'buddy-paste.html').read()+'</body>')  # 📥 paste-settings button (2026-10-17)
open(K+'intro-previz.html','w').write(html); print('previz v1.3',len(html)//1024,'KB'); print(json.dumps(F))
js=re.search(r'<script>(.*?)</script>',html,re.S).group(1); t=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False); t.write(js); t.close()
r=subprocess.run(['node','--check',t.name],capture_output=True,text=True); print('node --check:','OK' if r.returncode==0 else r.stderr[:400])
