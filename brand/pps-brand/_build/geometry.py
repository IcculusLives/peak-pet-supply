"""PPS geometry — source of truth for every file in the package.
Emblem (dog on the peak): the shipped site SVGs only wrap a flat-color 1096x536 PNG, so it is REBUILT here as true vector:
alpha channel -> 2x zoom + gaussian(1.2, mode=constant) -> potrace (alpha 1.0, opt 0.3, turd 30) in the 548x486 lockup space
the site files already use (scale 0.25 from trace px). Dog / mountain and left / center / right peaks are split by a watershed on the
distance transform (cores = opening with a 50-px disk), so the cuts land at the thinnest necks (the paws, the ridge saddles).
Wordmark: the shipped paths are already true vector outlines (Montserrat ExtraBold / Medium, "1e" lockup 2026-07-21) and are copied verbatim:
LIGHT set (logo-final: text on the gold box) and DARK set (logo-white / logo-outline: heavier weights for dark grounds), plus the
type-only horizontal wordmark (wordmark-horizontal.svg, 617.6x107). Output: geometry.json."""
import numpy as np, subprocess, re, json, os, base64, io
from PIL import Image
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from skimage.morphology import disk, opening
from svgpathtools import parse_path
HERE=os.path.dirname(os.path.abspath(__file__))+'/'
REPO=os.path.abspath(HERE+'../../..')+'/'
IMG=REPO+'img/'
DATE='2026-09-16'
UNITS=[548,486]
# ---- locked values ----
COLORS={'navy':'#0E2433','blue':'#10689A','gold':'#F6C808','offwhite':'#F8F8F8','cream':'#f2efe9','gold_link':'#B8860B','gold_button':'#E5B94E','forest':'#161b1b'}
BOX=dict(x=19.5,y=269.5,w=509,h=209,rx=14,stroke=3)          # wordmark box as shipped (fill or 3-unit stroke)
OPEN_R=50; ZOOM=2; SMOOTH=1.2
def paths_of(f):
    t=open(IMG+f).read(); return t,re.findall(r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})"',t)
svg_final,wm_light=paths_of('logo-final.svg'); svg_white,wm_dark=paths_of('logo-white.svg'); _,wm_h=paths_of('wordmark-horizontal.svg')
assert len(wm_light)==2 and len(wm_dark)==2 and len(wm_h)==3
b64=re.search(r'href="data:image/png;base64,([^"]+)"',svg_final).group(1)
img=Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGBA'); assert img.size==(1096,536)
A=np.array(img)[...,3].astype(float)/255
m=ndi.gaussian_filter(ndi.zoom(A,ZOOM,order=3),SMOOTH,mode='constant')>0.5
H,W=m.shape
core=opening(m,disk(OPEN_R)); cl,cn=ndi.label(core)
markers=np.zeros(m.shape,int)                                 # 1 mountain-left 2 mountain-center 3 mountain-right 4 dog
for i in range(1,cn+1):
    ys,xs=np.where(cl==i); cx=xs.mean()
    if ys.max()<H*0.8: markers[cl==i]=4
    else: markers[cl==i]=1 if cx<W*0.30 else (3 if cx>W*0.70 else 2)
ws=watershed(-ndi.distance_transform_edt(m),markers,mask=m)
K=0.5/ZOOM
def trace(mask,name,turd=30):
    os.makedirs(HERE+'masks',exist_ok=True); p=HERE+f'masks/{name}.pbm'
    Image.fromarray((~mask).astype(np.uint8)*255).convert('1').save(p)
    out=subprocess.run(['potrace','-s','--flat','-u','10','-a','1.0','-O','0.3','-t',str(turd),'-o','-',p],capture_output=True,text=True,check=True).stdout
    d=re.search(r'<path[^>]*d="([^"]+)"',out,re.S).group(1)
    tx,ty,sx,sy=map(float,re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)',out).groups())
    toks=re.findall(r'[MmLlCcZz]|-?\d+(?:\.\d+)?',d); res=[]; cmd=None; nums=[]
    def flush():
        if cmd and nums:
            pts=[((tx+sx*nums[j])*K,(ty+sy*nums[j+1])*K) if cmd=='M' else (sx*nums[j]*K,sy*nums[j+1]*K) for j in range(0,len(nums),2)]
            res.append(cmd+' '.join(f"{x:.2f},{y:.2f}" for x,y in pts))
    for t in toks:
        if t.isalpha():
            flush(); nums=[]
            if t in 'Zz': res.append('Z'); cmd=None
            else: cmd=t
        else: nums.append(float(t))
    flush(); return ' '.join(res)
def bbox(mask):
    ys,xs=np.where(mask); return [round(xs.min()*K,2),round(ys.min()*K,2),round((xs.max()+1)*K,2),round((ys.max()+1)*K,2)]
def pbbox(d):
    x0,x1,y0,y1=parse_path(d).bbox(); return [round(x0,2),round(y0,2),round(x1,2),round(y1,2)]
geo={'source':{'emblem_raster':'img/logo-final.svg (embedded PNG 1096x536)','wordmark_light':'img/logo-final.svg','wordmark_dark':'img/logo-white.svg','wordmark_horizontal':'img/wordmark-horizontal.svg','benchmark':['img/elevation-benchmark.svg','img/elevation-benchmark-bronze.svg']},
     'units':UNITS,'generated':DATE,'colors':COLORS,'box':BOX,'trace':{'zoom':ZOOM,'smooth':SMOOTH,'open_r':OPEN_R,'potrace':'-a 1.0 -O 0.3 -t 30'},
     'parts':{}}
for name,mask in (('emblem',m),('dog',ws==4),('mountain',(ws>=1)&(ws<=3)),('mountain-left',ws==1),('mountain-center',ws==2),('mountain-right',ws==3)):
    geo['parts'][name]={'d':trace(mask,name),'bbox':bbox(mask)}
for name,(d,_) in zip(('peak','pet-supply'),wm_light): geo['parts'][name]={'d':d,'bbox':pbbox(d)}
for name,(d,_) in zip(('peak-dark','pet-supply-dark'),wm_dark): geo['parts'][name]={'d':d,'bbox':pbbox(d)}
for name,(d,_) in zip(('h-peak','h-pet','h-supply'),wm_h): geo['parts'][name]={'d':d,'bbox':pbbox(d)}
def union(*names):
    bs=[geo['parts'][n]['bbox'] for n in names]; return [min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs)]
geo['bbox']={'emblem':geo['parts']['emblem']['bbox'],'dog':geo['parts']['dog']['bbox'],'mountain':geo['parts']['mountain']['bbox'],
  'wordmark':union('peak','pet-supply','peak-dark','pet-supply-dark'),'peak':union('peak','peak-dark'),'pet-supply':union('pet-supply','pet-supply-dark'),
  'box':[BOX['x']-BOX['stroke']/2,BOX['y']-BOX['stroke']/2,BOX['x']+BOX['w']+BOX['stroke']/2,BOX['y']+BOX['h']+BOX['stroke']/2],
  'wordmark-h':union('h-peak','h-pet','h-supply')}
for k in ('mountain-left','mountain-center','mountain-right'): geo['bbox'][k]=geo['parts'][k]['bbox']
e,b=geo['bbox']['emblem'],geo['bbox']['box']; geo['bbox']['lockup']=[min(e[0],b[0]),e[1],max(e[2],b[2]),b[3]]
_ys,_xs=np.where(ws==2); geo['bbox']['summit']=[round(float(_xs[np.argmin(_ys)])*K,2),round(float(_ys.min())*K,2)]   # highest mountain pixel = where the dog stands
geo['bbox']['ground_y']=geo['bbox']['emblem'][3]
_dy,_dx=np.where(ws==4); _top=_dy.min(); _sel=_dy<_top+0.30*(_dy.max()-_top); _sx=_dx[_sel].max(); _sy=_dy[_sel][_dx[_sel]==_sx].mean()
geo['bbox']['snout']=[round(float(_sx)*K,2),round(float(_sy)*K,2)]   # dog's nose tip — origin of the vocal sound-wave arcs
json.dump(geo,open(HERE+'geometry.json','w'))
print({k:v for k,v in geo['bbox'].items()})
print('subpaths',{k:v['d'].count('M')+v['d'].count('m') for k,v in geo['parts'].items() if 'mountain' in k or k in('dog','emblem')})
# proof of the split
rgb=np.zeros(m.shape+(3,),np.uint8)+235
for v,c in ((1,(60,120,180)),(2,(16,104,154)),(3,(90,150,200)),(4,(230,120,30))): rgb[ws==v]=c
Image.fromarray(rgb).resize((W//2,H//2)).save(HERE+'split-proof.png')
