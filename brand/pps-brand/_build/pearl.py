"""pearl.py — the 'pearl' logo variants: the dog wearing the boa (static pose of the v1.5 ident boa, fully grown, tail at rest).
Reads an existing master, inserts <g id="boa-back"> before the dog path and <g id="boa-front"> after it, writes pps-<part>-<variant>-pearl.svg.
Boa geometry = previz boa() at u=1 (ae-kit/PPS-MOTION-SPEC.md v1.5), converted from comp px to lockup units (/1.895317, -offset)."""
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))+'/'; M=HERE+'../masters/'
S=1.895317; OX,OY=440.683,60.248
def u(x,y): return ((x-OX)/S, (y-OY)/S)
NECK=(1006,190); RX,RY=43,15; TILT=24*math.pi/180; ct,st=math.cos(TILT),math.sin(TILT)
PINKS=['#FF3D9A','#FF6FB5','#FF8FC8','#FFB3DA','#F0197F']; HI='#FFD6EC'
def h1(i): x=math.sin(i*12.9898+78.233)*43758.5453; return x-math.floor(x)
def P(phi): x=RX*math.cos(phi); y=RY*math.sin(phi); return (NECK[0]+x*ct-y*st, NECK[1]+x*st+y*ct)
def tuft(x,y,r,col,nz2=None,amt=1.0):
    ux,uy=u(x,y); r/=S; s=''
    for k,o in ((1.7,0.22),(1.25,0.45),(1.0,0.95)): s+=f'<circle cx="{ux:.2f}" cy="{uy:.2f}" r="{r*k:.2f}" fill="{col}" opacity="{o*amt:.2f}"/>'
    if nz2 is not None and nz2>0.55: s+=f'<circle cx="{ux+r*0.35*(nz2-0.5):.2f}" cy="{uy-r*0.3:.2f}" r="{r*0.42:.2f}" fill="{HI}" opacity="{0.55*amt:.2f}"/>'
    return s
def star(x,y,s,op=0.85):
    ux,uy=u(x,y); s/=S
    return f'<path d="M{ux:.2f},{uy-s:.2f} Q{ux:.2f},{uy:.2f} {ux+s:.2f},{uy:.2f} Q{ux:.2f},{uy:.2f} {ux:.2f},{uy+s:.2f} Q{ux:.2f},{uy:.2f} {ux-s:.2f},{uy:.2f} Q{ux:.2f},{uy:.2f} {ux:.2f},{uy-s:.2f}Z" fill="#FFFFFF" opacity="{op:.2f}"/>'
def boa(tail=78):
    back=front=spark=''; T=24
    for k in range(T+1):
        d=(k/T)*math.pi
        for dr in (1,-1):
            phi=math.pi+dr*d; i=k if dr>0 else T*2+5-k; x,y=P(phi); nz,nz2=h1(i),h1(i+97)
            r=(10+5*nz)+1; col=PINKS[i%5]; c=tuft(x,y,r,col,nz2)
            if math.sin(phi)>0: front+=c
            else: back+=c
            if nz>0.62 and h1(i+31)>0.45: spark+=star(x+(nz2-0.5)*2*r, y+(nz-0.5)*2*r, (5+6*nz)*0.8)
    bx0,by0=P(0); n=max(2,round(tail/8))
    for k in range(1,n+1):
        q=k/n; nz,nz2=h1(900+k),h1(997+k); r=((10+5*nz)*(1-0.35*q)+(10 if k==n else 0)); col=PINKS[(k+2)%5]
        x=bx0+(nz-0.5)*3; y=by0+tail*q; front+=tuft(x,y,r,col)
        if nz2>0.6 and k%2: spark+=star(x,y,(4+5*nz2)*0.8)
    return back, front+spark
def make(src,name):
    s=open(M+src,encoding='utf-8').read(); m=re.search(r'<path id="dog-[^"]*"[^>]*/>',s); assert m, src
    back,front=boa(); b=f'<g id="boa-back-{name}">{back}</g>'; f=f'<g id="boa-front-{name}">{front}</g>'
    s=s[:m.start()]+b+m.group(0)+f+s[m.end():]
    s=s.replace('vector master, generated','pearl variant (the dog wearing the ident boa, _build/pearl.py 2026-10-20) of the vector master generated',1)
    out=M+f'pps-{name}-pearl.svg'; open(out,'w',encoding='utf-8').write(s); print('wrote',out, len(s)//1024,'KB')
for src,name in [('pps-lockup-vertical-on-navy-color.svg','lockup-vertical-on-navy-color'),('pps-lockup-vertical.svg','lockup-vertical'),('pps-mark-on-dark.svg','mark-on-dark'),('pps-mark.svg','mark'),('pps-dog-on-dark.svg','dog-on-dark'),('pps-dog.svg','dog')]:
    make(src,name)
