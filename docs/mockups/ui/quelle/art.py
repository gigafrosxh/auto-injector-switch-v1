# Erzeugt Hintergrund- und Kachelgrafiken (abstrakt, eigen) als PNG
from PIL import Image, ImageDraw, ImageFilter
import random, math, os
os.makedirs('art', exist_ok=True)
def grad(w,h,c1,c2,angle=0):
    im=Image.new('RGB',(w,h)); px=im.load()
    for y in range(h):
        for x in range(0,w):
            t=(x*math.cos(angle)+y*math.sin(angle))/(w*abs(math.cos(angle))+h*abs(math.sin(angle)))
            t=max(0,min(1,t))
            px[x,y]=tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))
    return im
def glow(im,cx,cy,r,col,a):
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=col+(a,)); g=g.filter(ImageFilter.GaussianBlur(r*0.45))
    im.alpha_composite(g)
def rings(im,cx,cy,rx,ry,col,w,n=3,a=60):
    o=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(o)
    for i in range(n):
        k=1+i*0.22; d.ellipse([cx-rx*k,cy-ry*k,cx+rx*k,cy+ry*k],outline=col+(int(a/(i+1)),),width=w)
    im.alpha_composite(o)
def planet(im,cx,cy,r,c1,c2):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
    g=grad(im.size[0],im.size[1],c1,c2,0.9).convert('RGBA')
    im.paste(g,(0,0),m)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).ellipse([cx-r*0.35,cy-r*0.2,cx+r*1.9,cy+r*1.9],fill=(6,8,24,170))
    sh=sh.filter(ImageFilter.GaussianBlur(r*0.18)); sa=sh.split()[3]
    sh.putalpha(Image.composite(sa,Image.new('L',im.size,0),m))
    im.alpha_composite(sh)
def stars(im,n,seed):
    random.seed(seed); d=ImageDraw.Draw(im)
    for _ in range(n):
        x,y=random.randrange(im.size[0]),random.randrange(im.size[1]); b=random.randint(90,230); s=random.choice([1,1,1,2])
        d.ellipse([x,y,x+s,y+s],fill=(b,b,min(255,b+20)))
W,H=1920,1080
# Startbildschirm
im=grad(W,H,(8,10,26),(32,14,52),0.7).convert('RGBA'); stars(im,260,1)
glow(im,1450,330,520,(62,224,197),70); glow(im,300,950,500,(233,84,32),45)
rings(im,1450,380,470,120,(236,238,245),4,3,110)
planet(im,1450,380,260,(62,224,197),(40,120,190))
front=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(front).arc([1450-470,380-120,1450+470,380+120],0,180,fill=(236,238,245,200),width=5); im.alpha_composite(front)
im.convert('RGB').save('art/home.jpg',quality=88)
# Login
im=grad(W,H,(10,12,30),(14,30,44),1.2).convert('RGBA'); stars(im,320,2)
glow(im,960,1250,900,(62,224,197),60); glow(im,1700,150,400,(150,90,255),40)
rings(im,960,1350,1100,520,(62,224,197),3,4,90)
im.convert('RGB').save('art/login.jpg',quality=88)
# Kacheln (App-Art)
def tile(name,c1,c2,shape,seed):
    w,h=800,450; base=grad(w,h,c1,c2,0.6).convert('RGBA'); random.seed(seed)
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    if shape=='orbit':
        rings(im,560,220,260,70,(255,255,255),5,3,150); d=ImageDraw.Draw(im); d.ellipse([490,150,630,290],fill=(255,255,255,235))
    elif shape=='grid':
        for i in range(9):
            for j in range(5):
                if random.random()<.55: d.rounded_rectangle([60+i*80,40+j*80,120+i*80,100+j*80],12,fill=(255,255,255,random.randint(25,90)))
    elif shape=='wave':
        for k in range(7):
            pts=[(x,260+60*math.sin(x/90+k*0.7)-k*28) for x in range(0,w+10,10)]
            d.line(pts,fill=(255,255,255,40+k*20),width=6)
    elif shape=='mount':
        for k,(c,o) in enumerate([((255,255,255,50),0),((255,255,255,90),60),((20,10,40,200),130)]):
            pts=[(0,h)]+[(x,280+o-120*abs(math.sin(x/170+k))) for x in range(0,w+20,20)]+[(w,h)]
            d.polygon(pts,fill=c)
        d.ellipse([560,60,660,160],fill=(255,240,200,230))
    elif shape=='code':
        for j in range(9):
            x=60+random.randint(0,3)*40; d.rounded_rectangle([x,50+j*40,x+random.randint(120,420),70+j*40],8,fill=(255,255,255,random.randint(60,160)))
    elif shape=='blocks':
        for _ in range(14):
            x,y,s=random.randint(0,w),random.randint(0,h),random.randint(40,140)
            d.rounded_rectangle([x,y,x+s,y+s],s//5,fill=(255,255,255,random.randint(20,80)))
    elif shape=='speed':
        for _ in range(26):
            y=random.randint(0,h); x=random.randint(-200,w); L=random.randint(120,420)
            d.line([(x,y),(x+L,y-L*0.35)],fill=(255,255,255,random.randint(40,140)),width=random.randint(2,7))
    elif shape=='film':
        for i in range(6): d.rounded_rectangle([40+i*125,120,140+i*125,330],14,fill=(255,255,255,50+i*15))
    base.alpha_composite(im); base.convert('RGB').save(f'art/{name}.jpg',quality=86)
tile('t-orbit',(26,40,90),(62,224,197),'orbit',1)
tile('t-sterne',(60,20,90),(233,84,32),'speed',2)
tile('t-pixel',(12,90,80),(160,230,120),'blocks',3)
tile('t-berg',(240,140,70),(120,40,110),'mount',4)
tile('t-code',(20,24,40),(60,80,160),'code',5)
tile('t-wellen',(10,60,120),(40,190,230),'wave',6)
tile('t-raster',(90,30,60),(240,90,120),'grid',7)
tile('t-film',(30,30,30),(120,120,140),'film',8)
# Store-Banner
tile('b-code',(16,20,44),(62,120,200),'code',9)
print('ok')
