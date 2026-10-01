"""brand-sheet.html — one self-contained page (inline SVG, no external files)."""
import os, re
from lib import *
OUT=os.path.abspath(HERE+'..')+'/'
def inl(name,h=None,uid=''):
    t=open(OUT+'masters/pps-'+name+'.svg').read(); t=t[t.index('<svg'):]
    t=re.sub(r'\s(width|height)="[^"]+"','',t,count=2)
    if uid: t=re.sub(r'id="([^"]+)"',lambda m:f'id="{uid}-{m.group(1)}"',t); t=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{uid}-{m.group(1)})',t); t=re.sub(r'xlink:href="#([^"]+)"',lambda m:f'xlink:href="#{uid}-{m.group(1)}"',t)
    return f'<div class="art" style="height:{h or 180}px">{t}</div>'
def card(title,art,note='',dark=False): return f'<div class="card{" dark" if dark else ""}"><div class="ttl">{title}</div>{art}<div class="note">{note}</div></div>'
sw=lambda n,hexv,role: f'<div class="sw"><div class="chip" style="background:{hexv}"></div><b>{n}</b><code>{hexv}</code><span>{role}</span></div>'
x0,y0,x1,y1=BB['lockup']; dx0,dy0,dx1,dy1=BB['dog']; X=round(dy1-dy0,1)   # clearspace unit X = height of the dog
cs=f'''<svg viewBox="{x0-X-20} {y0-X-20} {x1-x0+2*X+40} {y1-y0+2*X+40}" style="height:360px;display:block;margin:auto">
<rect x="{x0-X}" y="{y0-X}" width="{x1-x0+2*X}" height="{y1-y0+2*X}" fill="none" stroke="#c33" stroke-dasharray="6 5" stroke-width="1.5"/>
{parts(PRIMARY,('emblem','box','wordmark'),'-cs')}
<rect x="{dx0}" y="{dy0}" width="{dx1-dx0}" height="{dy1-dy0}" fill="none" stroke="#c33" stroke-width="1.5"/><text x="{dx1+6}" y="{(dy0+dy1)/2}" font-size="22" fill="#c33" font-family="sans-serif">X = dog height ({X} u)</text>
<text x="{x0-X+8}" y="{y0-X-8}" font-size="18" fill="#c33" font-family="sans-serif">clearspace = X on every side</text></svg>'''
html=f'''<!doctype html><html><head><meta charset="utf-8"><title>Peak Pet Supply — brand sheet</title>
<style>
body{{margin:0;background:#fff;color:#1a1a1a;font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif}} .wrap{{max-width:1100px;margin:0 auto;padding:40px 28px 80px}}
h1{{font-size:34px;margin:0 0 4px}} .sub{{color:#666;margin-bottom:28px}} h2{{font-size:20px;margin:44px 0 12px;border-bottom:2px solid {GOLD};padding-bottom:4px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}} .card{{border:1px solid #e3e3e3;border-radius:10px;padding:12px;background:{CREAM}}} .card.dark{{background:{NAVY};color:#ddd;border-color:#333}}
.ttl{{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#888;margin-bottom:8px}} .card.dark .ttl{{color:#9ab}} .note{{font-size:12px;color:#777;margin-top:8px}}
.art svg{{width:100%;height:100%}} .hero{{background:{NAVY};border-radius:14px;padding:40px}} .hero .art{{height:420px}}
.sws{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}} .sw .chip{{height:56px;border-radius:8px;border:1px solid #ddd}} .sw b{{display:block;margin-top:6px}} .sw code{{display:block;color:#555}} .sw span{{font-size:12px;color:#777}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid #e5e5e5;padding:7px 9px;text-align:left;vertical-align:top}} th{{background:#f4f4f4}}
.dd{{display:grid;grid-template-columns:1fr 1fr;gap:20px}} .dd ul{{margin:0;padding-left:18px}} code{{font-family:Menlo,monospace;font-size:13px}}
@media print{{ .wrap{{padding:0}} .card{{break-inside:avoid}} }}
</style></head><body><div class="wrap">
<h1>Peak Pet Supply</h1><div class="sub">Brand sheet · vector masters v1 · {DATE} · <code>brand/pps-brand/</code> in the site repo. <b>Source of truth is vector:</b> the emblem was rebuilt with potrace from the flat raster the site SVGs embedded; the wordmark keeps its shipped Montserrat outlines. Nothing here needs a font.</div>
<div class="hero">{inl('lockup-vertical-on-navy-color',420)}</div>
<h2>Primary mark</h2><div class="grid">{card('Vertical · light grounds',inl('lockup-vertical'),'pps-lockup-vertical.svg')}{card('Vertical · dark grounds',inl('lockup-vertical-on-dark'),'pps-lockup-vertical-on-dark.svg (the site header)',True)}{card('Vertical · outline',inl('lockup-vertical-outline'),'pps-lockup-vertical-outline.svg')}
{card('Horizontal · boxed',inl('lockup-horizontal',120),'box = 80 % of emblem height, gap 10 %')}{card('Horizontal · type',inl('lockup-horizontal-type',120),'nav / email: type at 42 % of emblem height')}{card('Horizontal · on navy',inl('lockup-horizontal-on-navy',120),'full-color scheme: offwhite emblem + gold box',True)}</div>
<h2>Mark, dog, wordmark</h2><div class="grid">{card('Emblem',inl('mark',140),'dog on the peak — rebuilt vector, one path')}{card('Dog alone',inl('dog',140),'favicon / avatar glyph')}{card('Wordmark · boxed',inl('wordmark-boxed',120),'')}{card('Wordmark · unboxed',inl('wordmark',110),'navy on light')}{card('Wordmark · horizontal',inl('wordmark-horizontal',90),'PEAK + stacked PET / SUPPLY')}{card('Benchmark badge (secondary)',inl('benchmark-gold',180,'bg'),'9,217 ft · Black Hawk, CO · gold + bronze')}</div>
<h2>One color</h2><div class="grid">{card('Mono black',inl('lockup-vertical-mono-black'),'')}{card('Mono white',inl('lockup-vertical-mono-white'),'',True)}{card('Mono navy',inl('lockup-vertical-mono-navy'),'')}{card('Mono gold',inl('lockup-vertical-mono-gold'),'')}</div>
<h2>Color</h2><div class="sws">{sw('Navy',NAVY,'ground, icons, wordmark on light')}{sw('Brand blue',BLUE,'emblem on light')}{sw('Gold',GOLD,'wordmark box')}{sw('Off-white',OFFWHITE,'emblem + type on dark')}{sw('Cream',CREAM,'light ground')}{sw('Forest',FOREST,'site header/footer ground')}{sw('Gold (links)',C['gold_link'],'site links')}{sw('Gold (buttons)',C['gold_button'],'site buttons')}</div>
<h2>Clearspace &amp; minimum size</h2>{cs}
<table><tr><th>Use</th><th>Minimum width</th></tr><tr><td>Screen, full color (vertical lockup)</td><td>120 px</td></tr><tr><td>Screen, one color</td><td>100 px</td></tr><tr><td>Print</td><td>25 mm</td></tr><tr><td>Below that</td><td>use the emblem alone; below 32 px use the dog glyph (icons/pps-favicon-dog)</td></tr></table>
<h2>Construction system</h2><table><tr><th>Item</th><th>Value (lockup units, 548 × 486)</th></tr>
<tr><td>Emblem bbox</td><td>{BB['emblem']}</td></tr><tr><td>Dog bbox / summit</td><td>{BB['dog']} · summit at {BB['summit']}</td></tr><tr><td>Box</td><td>x {BOX['x']} y {BOX['y']} w {BOX['w']} h {BOX['h']} rx {BOX['rx']} · outline stroke {BOX['stroke']}</td></tr>
<tr><td>Wordmark sets</td><td>LIGHT (thinner, on the gold box) and DARK (heavier, for outline/dark grounds) — both shipped outlines, chosen by scheme</td></tr><tr><td>Horizontal lockup</td><td>box height 80 % of emblem height, gap 10 %; type lockup 42 % / 10 %</td></tr>
<tr><td>Trace</td><td>2× zoom, gaussian 1.2 (mode constant), potrace -a 1.0 -O 0.3 -t 30; dog/mountain + 3 peaks split by watershed on the distance transform (opening r = 50 px)</td></tr></table>
<h2>Typography</h2><p>Wordmark: <b>Montserrat</b> ExtraBold (PEAK) / Medium (PET SUPPLY), shipped as outlines — no font needed. Site UI: <b>Barlow</b> + Barlow Condensed. Copy casing: <i>Peak Pet Supply</i>; art is all caps.</p>
<h2>Do / Don't</h2><div class="dd"><div><b>Do</b><ul><li>Use <code>-on-dark</code> files on dark grounds, transparent <code>lockup-vertical</code> on light.</li><li>Use the full-color scheme (offwhite emblem + gold box) on navy for hero/social.</li><li>Keep clearspace = the dog's height on every side.</li><li>Regenerate from <code>_build/</code> when a value changes.</li></ul></div>
<div><b>Don't</b><ul><li>Don't put the light-ground file on dark (blue emblem vanishes on navy).</li><li>Don't reset the wordmark in another font or re-kern it.</li><li>Don't restroke the outline box or scale the box and text separately.</li><li>Don't use the old <code>img/logo*.svg</code> as a source — they wrap a PNG.</li></ul></div></div>
<h2>Motion</h2><p>"Summit" ident — comp <code>PPS_Summit</code> 1920×1080 @ 30 fps, 435 f (14.5 s). Peaks rise on the bed, the dog lands on the 808, the gold box slams, PEAK pops, PET SUPPLY wipes on. Previz <code>ae-kit/intro-previz.html</code> (⚙︎ tune: every audio start, gain and hit is a slider), spec <code>ae-kit/PPS-MOTION-SPEC.md</code>, registration <code>ae-kit/parts/registration.json</code>.</p>
<h2>File map</h2><table><tr><th>Folder</th><th>Contents</th></tr><tr><td><code>masters/</code></td><td>38 SVG masters: lockups (vertical / horizontal / type), marks, dog, wordmarks, mono set, benchmark badges</td></tr><tr><td><code>png/</code></td><td>renders 1000 / 2000 / 4000 w, marks 1024 / 2048 / 4096</td></tr><tr><td><code>icons/</code></td><td>app/favicon set 16–1024, maskable, apple-touch, ios, favicon.ico, dog-glyph favicon, benchmark icon</td></tr><tr><td><code>social/</code></td><td>avatars, YouTube / X / Facebook / LinkedIn / OG / Instagram (SVG + PNG)</td></tr><tr><td><code>ae-kit/</code></td><td>parts in comp space, registration.json, timeline.json, previz, spec</td></tr><tr><td><code>_build/</code></td><td>geometry.py → geometry.json → lib.py → export.py / ae.py / gen_previz.py / gen_sheet.py; contact.jpg proof</td></tr></table>
</div></body></html>'''
open(OUT+'brand-sheet.html','w').write(html); print('brand-sheet.html',len(html)//1024,'KB')
