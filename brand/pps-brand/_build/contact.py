"""Contact sheet of every master + icons + social so a wrong mask / bleached recolor is obvious at a glance."""
import glob, os, subprocess
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__))+'/'; OUT=os.path.abspath(HERE+'..')+'/'
items=sorted(glob.glob(OUT+'masters/*.svg'))+sorted(glob.glob(OUT+'icons/*.svg'))+sorted(glob.glob(OUT+'social/*.svg'))
CW,CH,COLS=300,240,6; rows=(len(items)+COLS-1)//COLS
sheet=Image.new('RGB',(COLS*CW,rows*CH),(200,200,200)); d=ImageDraw.Draw(sheet)
for i,f in enumerate(items):
    tmp=HERE+'_c.png'; subprocess.run(['rsvg-convert','-w',str(CW-20),'-h',str(CH-40),'--keep-aspect-ratio',f,'-o',tmp],check=True)
    im=Image.open(tmp).convert('RGBA'); x,y=(i%COLS)*CW,(i//COLS)*CH
    # checker-ish grounds: light for *-on-dark / mono-white use dark, else light
    dark=any(k in f for k in ('on-dark','mono-white','favicon','icon.svg','icon-square','maskable'))
    bg=(40,44,48) if dark else (238,236,230)
    tile=Image.new('RGBA',(CW-20,CH-40),bg+(255,)); tile.alpha_composite(im,((tile.width-im.width)//2,(tile.height-im.height)//2))
    sheet.paste(tile.convert('RGB'),(x+10,y+30)); d.text((x+10,y+8),os.path.basename(f)[:44],fill=(0,0,0))
os.remove(tmp); sheet.save(HERE+'contact.jpg',quality=85); print(len(items),'tiles ->',HERE+'contact.jpg')
