"""masters/ png/ icons/ social/ from geometry.json. Run from anywhere: python3 _build/export.py (needs rsvg-convert + Pillow)."""
import os, subprocess, json, re, sys
from lib import *
OUT=os.path.abspath(HERE+'..')+'/'; REPO=os.path.abspath(HERE+'../../..')+'/'
for d in ('masters','png','icons','social','ae-kit/parts','_build'): os.makedirs(OUT+d,exist_ok=True)
files={}; ALL=('emblem','box','wordmark'); BOXED=('box','wordmark')
def vert(name,s,include,bg=None,pad=0.05):
    body,w,h,vb=tight(s,include,pad,bg,uid='-'+name); files[f'masters/pps-{name}.svg']=svg(w,h,body,name,vb)
vert('lockup-vertical',PRIMARY,ALL); vert('lockup-vertical-on-dark',ON_DARK,ALL); vert('lockup-vertical-outline',OUTLINE,ALL)
vert('lockup-vertical-on-navy',ON_DARK,ALL,NAVY,0.12); vert('lockup-vertical-on-navy-color',NAVY_COLOR,ALL,NAVY,0.12); vert('lockup-vertical-on-cream',PRIMARY,ALL,CREAM,0.12)
for n,c in (('black','#000000'),('white','#FFFFFF'),('navy',NAVY),('blue',BLUE),('gold',GOLD)): vert(f'lockup-vertical-mono-{n}',MONO(c),ALL)
vert('mark',PRIMARY,('emblem',)); vert('mark-on-dark',ON_DARK,('emblem',)); vert('mark-on-navy',ON_DARK,('emblem',),NAVY,0.15); vert('mark-on-cream',PRIMARY,('emblem',),CREAM,0.15)
for n,c in (('black','#000000'),('white','#FFFFFF'),('navy',NAVY),('gold',GOLD)): vert(f'mark-mono-{n}',MONO(c),('emblem',))
vert('dog',PRIMARY,('dog',)); vert('dog-on-dark',ON_DARK,('dog',))
vert('wordmark-boxed',PRIMARY,BOXED); vert('wordmark-boxed-on-dark',ON_DARK,BOXED); vert('wordmark-boxed-outline',OUTLINE,BOXED)
vert('wordmark',MONO(NAVY),('wordmark',)); vert('wordmark-on-dark',ON_DARK,('wordmark',))
for name,col in (('wordmark-horizontal',NAVY),('wordmark-horizontal-on-dark',OFFWHITE)):
    x0,y0,x1,y1=BB['wordmark-h']; pad=(y1-y0)*0.05; w,h=round(x1-x0+2*pad,2),round(y1-y0+2*pad,2)
    files[f'masters/pps-{name}.svg']=svg(w,h,wordmark_h(col),name,f'{x0-pad:.2f} {y0-pad:.2f} {w} {h}')
for name,s,bg,kind in (('lockup-horizontal',PRIMARY,None,'box'),('lockup-horizontal-on-dark',ON_DARK,None,'box'),('lockup-horizontal-on-navy',NAVY_COLOR,NAVY,'box'),('lockup-horizontal-on-cream',PRIMARY,CREAM,'box'),
                       ('lockup-horizontal-mono-black',MONO('#000000'),None,'box'),('lockup-horizontal-mono-white',MONO('#FFFFFF'),None,'box'),
                       ('lockup-horizontal-type',TYPE_LIGHT,None,'type'),('lockup-horizontal-type-on-dark',TYPE_DARK,None,'type')):
    b,W,H=horiz_body(s,'-'+name,bg,0.12 if bg else 0.06,kind); files[f'masters/pps-{name}.svg']=svg(W,H,b,name)
# ---- benchmark badge (secondary mark): already outlined vector in img/, carried over with the package header ----
for name,src in (('benchmark-gold','img/elevation-benchmark.svg'),('benchmark-bronze','img/elevation-benchmark-bronze.svg')):
    t=open(REPO+src).read(); t=re.sub(r'^<\?xml[^>]*>\s*','',t)
    files[f'masters/pps-{name}.svg']=f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Peak Pet Supply — {name} (elevation benchmark, secondary mark) — outlined vector carried from {src}, packaged {DATE} -->\n'+t
# ---- icons: navy tile, emblem (2:1) fitted by WIDTH ----
def icon_svg(size,frac=0.80,bg=NAVY,rx_frac=0.2,s=ON_DARK,uid='i',include=('emblem',),by='width'):
    g,_=place_vertical(s,include,size/2,size/2,**{by:size*frac},uid=uid); return comp(size,size,g,'icon',bg,round(size*rx_frac))
files['icons/pps-icon.svg']=icon_svg(512); files['icons/pps-icon-square.svg']=icon_svg(512,0.80,NAVY,0)
files['icons/pps-icon-maskable.svg']=icon_svg(512,0.60,NAVY,0)
files['icons/pps-icon-cream.svg']=icon_svg(512,0.80,CREAM,0.2,PRIMARY,'ic')
files['icons/pps-favicon-dog.svg']=icon_svg(512,0.74,NAVY,0.2,ON_DARK,'fd',('dog',),'height')   # dog alone survives 16/32 px
files['icons/pps-icon-benchmark.svg']=files['masters/pps-benchmark-gold.svg']
# ---- social (navy ground, full-color scheme) ----
S={}
S['pps-avatar-1000']=(1000,1000,lambda: place_vertical(ON_DARK,('emblem',),500,500,width=780,uid='av')[0])
S['pps-avatar-cream-1000']=(1000,1000,lambda: place_vertical(PRIMARY,('emblem',),500,500,width=780,uid='avc')[0],CREAM)
S['pps-avatar-dog-1000']=(1000,1000,lambda: place_vertical(ON_DARK,('dog',),500,500,height=640,uid='avd')[0])
S['pps-youtube-banner-2560x1440']=(2560,1440,lambda: place_horizontal(NAVY_COLOR,1280,720,1300,'yt'))
S['pps-x-header-1500x500']=(1500,500,lambda: place_horizontal(NAVY_COLOR,750,250,980,'x'))
S['pps-facebook-cover-1640x624']=(1640,624,lambda: place_horizontal(NAVY_COLOR,820,312,1100,'fb'))
S['pps-linkedin-banner-1584x396']=(1584,396,lambda: place_horizontal(NAVY_COLOR,850,198,900,'li'))
S['pps-og-1200x630']=(1200,630,lambda: place_horizontal(NAVY_COLOR,600,315,900,'og'))
S['pps-instagram-post-1080']=(1080,1080,lambda: place_vertical(NAVY_COLOR,ALL,540,540,height=820,uid='ig')[0])
S['pps-instagram-story-1080x1920']=(1080,1920,lambda: place_vertical(NAVY_COLOR,ALL,540,960,width=820,uid='igs')[0])
for k,v in S.items():
    w,h,fn=v[:3]; bg=v[3] if len(v)>3 else NAVY; files[f'social/{k}.svg']=comp(w,h,fn(),k,bg)
files['social/pps-avatar-benchmark-1000.svg']=files['masters/pps-benchmark-gold.svg'].replace('width="480" height="480"','width="1000" height="1000"',1)
for k,v in files.items(): open(OUT+k,'w').write(v)
print(len(files),'svgs written')
# ---- PNG renders ----
def png(src,dst,w=None,h=None):
    a=['rsvg-convert',src,'-o',dst]+(['-w',str(w)] if w else [])+(['-h',str(h)] if h else []); subprocess.run(a,check=True)
M=OUT+'masters/pps-'
for n in ('lockup-vertical','lockup-vertical-on-dark','lockup-horizontal','lockup-horizontal-on-dark'):
    for w in (1000,2000,4000): png(M+n+'.svg',f'{OUT}png/pps-{n}-{w}w.png',w)
for n in ('lockup-vertical-outline','lockup-vertical-on-navy','lockup-vertical-on-navy-color','lockup-vertical-on-cream','lockup-vertical-mono-black','lockup-vertical-mono-white','lockup-vertical-mono-navy','lockup-vertical-mono-blue','lockup-vertical-mono-gold',
          'lockup-horizontal-on-navy','lockup-horizontal-on-cream','lockup-horizontal-mono-black','lockup-horizontal-mono-white','lockup-horizontal-type','lockup-horizontal-type-on-dark',
          'wordmark-boxed','wordmark-boxed-on-dark','wordmark-boxed-outline','wordmark','wordmark-on-dark','wordmark-horizontal','wordmark-horizontal-on-dark','dog','dog-on-dark'):
    png(M+n+'.svg',f'{OUT}png/pps-{n}-2000w.png',2000)
for n in ('mark','mark-on-dark','mark-on-navy','mark-on-cream','mark-mono-black','mark-mono-white','mark-mono-navy','mark-mono-gold'):
    for w in ((1024,2048,4096) if n=='mark' else (2048,)): png(M+n+'.svg',f'{OUT}png/pps-{n}-{w}.png',w)
for n in ('benchmark-gold','benchmark-bronze'):
    for w in (1024,2048): png(M+n+'.svg',f'{OUT}png/pps-{n}-{w}.png',w)
I=OUT+'icons/'
sys.path.insert(0,os.path.expanduser('~/.claude/skills/brand-asset-package/scripts'))
from render_png import icons as icon_set, ico
icon_set(I+'pps-icon.svg',I,'pps',NAVY)
png(I+'pps-icon-maskable.svg',I+'pps-icon-maskable-512.png',512)
for sz in (512,1024): png(I+'pps-icon-cream.svg',f'{I}pps-icon-cream-{sz}.png',sz)
for sz in (16,32,48,64): png(I+'pps-favicon-dog.svg',f'{I}pps-favicon-dog-{sz}.png',sz)
ico(I+'favicon-dog.ico',*[f'{I}pps-favicon-dog-{s}.png' for s in (16,32,48)])
for sz in (180,512,1024): png(I+'pps-icon-benchmark.svg',f'{I}pps-icon-benchmark-{sz}.png',sz)
for k in list(S)+['pps-avatar-benchmark-1000']: png(f'{OUT}social/{k}.svg',f'{OUT}social/{k}.png')
json.dump({'horizontal':{'KB':KB,'GAP':GAP,'W':HW,'H':HH,'KT':KT,'W_type':HTW}},open(HERE+'layout.json','w'),indent=1)
print('done')
