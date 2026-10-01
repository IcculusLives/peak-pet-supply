"""AE kit parts: every layer as its own SVG already placed in 1920x1080 comp space (+ a 1080x1920 vertical), and registration.json.
Ground for the ident is NAVY with the full-color scheme (offwhite emblem, gold box, offwhite type)."""
import json, os
from lib import *
OUT=os.path.abspath(HERE+'../ae-kit/parts')+'/'; os.makedirs(OUT,exist_ok=True)
CW,CH=1920,1080; LH=860.0; FPS=30; DUR=14.5; FRAMES=435
x0,y0,x1,y1=BB['lockup']; S=LH/(y1-y0)
OX,OY=(CW-(x1-x0)*S)/2-x0*S,(CH-LH)/2-y0*S
T=f'translate({OX:.4f},{OY:.4f}) scale({S:.6f})'
SC=NAVY_COLOR
def part(name,body,w=CW,h=CH,tr=T): open(OUT+name,'w').write(svg(w,h,f'<g transform="{tr}">{body}</g>',name))
def cb(b): c=[OX+b[0]*S,OY+b[1]*S,OX+b[2]*S,OY+b[3]*S]; return [round(v,1) for v in c]+[round((c[0]+c[2])/2,1),round((c[1]+c[3])/2,1)]
open(OUT+'00-bg-navy-1920x1080.svg','w').write(svg(CW,CH,f'<rect width="{CW}" height="{CH}" fill="{NAVY}"/>','bg'))
open(OUT+'00-bg-navy-1080x1920.svg','w').write(svg(1080,1920,f'<rect width="1080" height="1920" fill="{NAVY}"/>','bg'))
part('01-mountain-left.svg',P('mountain-left','mountain-left',OFFWHITE))
part('02-mountain-center.svg',P('mountain-center','mountain-center',OFFWHITE))
part('03-mountain-right.svg',P('mountain-right','mountain-right',OFFWHITE))
part('04-mountain.svg',P('mountain','mountain',OFFWHITE))                  # whole ridge (alternative to 01–03)
part('05-dog.svg',P('dog','dog',OFFWHITE))
part('06-box-gold.svg',box(SC))
part('07-peak.svg',P('peak','peak',OFFWHITE))
part('08-pet-supply.svg',P('pet-supply','pet-supply',OFFWHITE))
part('09-full-lockup.svg',parts(SC,('emblem','box','wordmark'),'-ae'))
SV=900/(x1-x0); part('10-full-lockup-vertical-1080x1920.svg',parts(SC,('emblem','box','wordmark'),'-aev'),1080,1920,f'translate({(1080-(x1-x0)*SV)/2-x0*SV:.4f},{(1920-(y1-y0)*SV)/2-y0*SV:.4f}) scale({SV:.6f})')
sx,sy=BB['summit']
reg={'comp':[CW,CH],'fps':FPS,'frames':FRAMES,'duration_s':DUR,'lockup_height':LH,'scale':round(S,6),'offset':[round(OX,3),round(OY,3)],
     'note':'bbox = [x0,y0,x1,y1,cx,cy] in comp px. Set each layer anchor to its center. ground_y = base of the emblem; summit = the peak the dog stands on.',
     'lockup':cb([x0,y0,x1,y1]),'emblem':cb(BB['emblem']),'mountain':cb(BB['mountain']),'mountain-left':cb(BB['mountain-left']),'mountain-center':cb(BB['mountain-center']),'mountain-right':cb(BB['mountain-right']),
     'dog':cb(BB['dog']),'box':cb(BB['box']),'peak':cb(BB['peak']),'pet-supply':cb(BB['pet-supply']),'wordmark':cb(BB['wordmark']),
     'ground_y':round(OY+BB['ground_y']*S,1),'snout':[round(OX+BB['snout'][0]*S,1),round(OY+BB['snout'][1]*S,1)],'summit':[round(OX+sx*S,1),round(OY+sy*S,1)],
     'vertical_1080x1920':{'scale':round(SV,6),'lockup_width':900}}
json.dump(reg,open(OUT+'registration.json','w'),indent=1)
print(json.dumps({k:reg[k] for k in ('scale','lockup','emblem','dog','box','ground_y','summit')}))
