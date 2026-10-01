"""Shared SVG builders for the PPS package. All coordinates in lockup units (548x486, the space the site SVGs use).
Every deliverable is assembled from geometry.json through parts(); colors live in SCHEMES, never inline in a builder."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))+'/'
G=json.load(open(HERE+'geometry.json')); BB=G['bbox']; PT=G['parts']; BOX=G['box']; C=G['colors']; DATE=G['generated']
NAVY,BLUE,GOLD,OFFWHITE,CREAM,FOREST=C['navy'],C['blue'],C['gold'],C['offwhite'],C['cream'],C['forest']
# scheme = dict(emblem=color | ('dog','mountain') tuple, box='fill'|'stroke'|None, boxc=color, text=color, textset='light'|'dark', textdark=color for the horizontal type)
def scheme(emblem,box,boxc,text,textset,dog=None): return dict(emblem=emblem,dog=dog or emblem,box=box,boxc=boxc,text=text,textset=textset)
PRIMARY   =scheme(BLUE,'fill',GOLD,OFFWHITE,'light')        # logo-final: light grounds
ON_DARK   =scheme(OFFWHITE,'stroke',OFFWHITE,OFFWHITE,'dark') # logo-white: the site header/footer
OUTLINE   =scheme(BLUE,'stroke',GOLD,BLUE,'dark')            # logo-outline
NAVY_COLOR=scheme(OFFWHITE,'fill',GOLD,OFFWHITE,'light')     # full-color on navy: white emblem + gold box (hero / social / intro)
def MONO(c): return scheme(c,'stroke',c,c,'dark')
TYPE_LIGHT=dict(PRIMARY,text=NAVY); TYPE_DARK=dict(ON_DARK)  # horizontal type lockups: navy type on light, offwhite on dark
def P(id_,name,fill,extra=''): return f'<path id="{id_}" d="{PT[name]["d"]}" fill="{fill}"{extra}/>'
def emblem(s,uid='',split=True):
    if split: return f'<g id="emblem{uid}">{P("mountain"+uid,"mountain",s["emblem"])}{P("dog"+uid,"dog",s["dog"])}</g>'
    return P('emblem'+uid,'emblem',s['emblem'])
def box(s,uid=''):
    if not s['box']: return ''
    if s['box']=='fill': return f'<rect id="box{uid}" x="{BOX["x"]}" y="{BOX["y"]}" width="{BOX["w"]}" height="{BOX["h"]}" rx="{BOX["rx"]}" fill="{s["boxc"]}"/>'
    return f'<rect id="box{uid}" x="{BOX["x"]}" y="{BOX["y"]}" width="{BOX["w"]}" height="{BOX["h"]}" rx="{BOX["rx"]}" fill="none" stroke="{s["boxc"]}" stroke-width="{BOX["stroke"]}"/>'
def wordmark(s,uid=''):
    sfx='' if s['textset']=='light' else '-dark'
    return f'<g id="wordmark{uid}">{P("peak"+uid,"peak"+sfx,s["text"])}{P("pet-supply"+uid,"pet-supply"+sfx,s["text"])}</g>'
def wordmark_h(color,uid=''):
    return f'<g id="wordmark-h{uid}">{P("h-peak"+uid,"h-peak",color)}{P("h-pet"+uid,"h-pet",color)}{P("h-supply"+uid,"h-supply",color)}</g>'
def parts(s,include=('emblem','box','wordmark'),uid=''):
    out=[]
    if 'emblem' in include: out.append(emblem(s,uid))
    if 'dog' in include: out.append(P('dog'+uid,'dog',s['dog']))
    if 'box' in include: out.append(box(s,uid))
    if 'wordmark' in include: out.append(wordmark(s,uid))
    return '\n'.join(o for o in out if o)
def svg(w,h,body,title,vb=None):
    vb=vb or f'0 0 {w} {h}'
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Peak Pet Supply — {title} — vector master, generated {DATE} from _build/geometry.json (emblem rebuilt with potrace; wordmark = shipped outlines) -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">\n{body}\n</svg>\n')
def bbox_of(include):
    keys={'emblem':'emblem','dog':'dog','box':'box','wordmark':'wordmark'}
    bs=[BB[keys[k]] for k in include]; return [min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs)]
def tight(s,include,pad_frac=0.05,bg=None,uid=''):
    x0,y0,x1,y1=bbox_of(include); pad=(y1-y0)*pad_frac
    w,h=round(x1-x0+2*pad,2),round(y1-y0+2*pad,2)
    bgr=f'<rect x="{x0-pad:.2f}" y="{y0-pad:.2f}" width="{w}" height="{h}" fill="{bg}"/>\n' if bg else ''
    return bgr+parts(s,include,uid),w,h,f'{x0-pad:.2f} {y0-pad:.2f} {w} {h}'
# ---- horizontal lockups: emblem left, boxed wordmark right (box 80 % of emblem height, gap 10 %) ----
ex0,ey0,ex1,ey1=BB['emblem']; EW,EH=ex1-ex0,ey1-ey0
bx0,by0,bx1,by1=BB['box']; KB=0.80*EH/(by1-by0); GAP=0.10*EH
BW,BH=(bx1-bx0)*KB,(by1-by0)*KB; HW,HH=EW+GAP+BW,EH
hx0,hy0,hx1,hy1=BB['wordmark-h']; KT=0.42*EH/(hy1-hy0); TW,TH=(hx1-hx0)*KT,(hy1-hy0)*KT; HTW=EW+GAP+TW
def horiz_body(s,uid,bg=None,pad=0.06,kind='box'):
    p=EH*pad
    if kind=='box':
        W,H=HW+2*p,HH+2*p; right=f'<g id="text-h{uid}" transform="translate({p+EW+GAP-bx0*KB:.3f},{p+(EH-BH)/2-by0*KB:.3f}) scale({KB:.5f})">{box(s,uid)}{wordmark(s,uid)}</g>'
    else:
        W,H=HTW+2*p,HH+2*p; right=f'<g id="text-h{uid}" transform="translate({p+EW+GAP-hx0*KT:.3f},{p+(EH-TH)/2-hy0*KT:.3f}) scale({KT:.5f})">{wordmark_h(s["text"],uid)}</g>'
    b=f'<rect width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>\n' if bg else ''
    b+=f'<g id="mark-h{uid}" transform="translate({p-ex0:.3f},{p-ey0:.3f})">{emblem(s,uid)}</g>\n'+right
    return b,round(W,2),round(H,2)
def place_vertical(s,include,cx,cy,width=None,height=None,uid=''):
    x0,y0,x1,y1=bbox_of(include); w,h=x1-x0,y1-y0; k=width/w if width else height/h
    return f'<g transform="translate({cx-w*k/2:.3f},{cy-h*k/2:.3f}) scale({k:.6f}) translate({-x0:.3f},{-y0:.3f})">{parts(s,include,uid)}</g>',k
def place_horizontal(s,cx,cy,width,uid='',kind='box'):
    b,W,H=horiz_body(s,uid,None,0,kind); k=width/W
    return f'<g transform="translate({cx-W*k/2:.3f},{cy-H*k/2:.3f}) scale({k:.6f})">{b}</g>'
def comp(w,h,inner,name,bg=NAVY,rx=0):
    return svg(w,h,f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>\n{inner}',name)
