from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random, math

OUT=Path(__file__).parent/'assets'; OUT.mkdir(exist_ok=True)
BG='#07110d'; PANEL='#0b1b12'; GRID='#122a1b'; MUTED='#668b72'; GREEN='#aaff59'; WHITE='#e7f9e9'; TEAL='#49d4a4'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
fonts={}
def font(n,b=False):
    k=(n,b)
    if k not in fonts: fonts[k]=ImageFont.truetype(BOLD if b else MONO,n)
    return fonts[k]
def text(d,xy,s,n=14,c=WHITE,b=False,anchor=None): d.text(xy,s,font=font(n,b),fill=c,anchor=anchor)
def base(w,h):
    im=Image.new('RGB',(w,h),BG); d=ImageDraw.Draw(im)
    for x in range(0,w,24): d.line((x,0,x,h),fill='#0d1e15')
    for y in range(0,h,24): d.line((0,y,w,y),fill='#0d1e15')
    d.rectangle((1,1,w-2,h-2),outline='#285038'); return im,d
def corners(d,w,h):
    for x,y,sx,sy in [(9,9,1,1),(w-10,9,-1,1),(9,h-10,1,-1),(w-10,h-10,-1,-1)]:
        d.line((x,y,x+sx*15,y),fill=GREEN,width=2); d.line((x,y,x,y+sy*15),fill=GREEN,width=2)
def gif(name,frames,duration=90):
    frames=[f.quantize(colors=96,method=Image.Quantize.MEDIANCUT) for f in frames]
    frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=True,disposal=2)
def line(d,pts,c=GREEN,w=1):d.line(pts,fill=c,width=w)

# 01 — animated identity, synthetic terminal visuals and orbiting data globe
frames=[]; W,H=920,300
rng=random.Random(26); streams=[(rng.randrange(0,24),rng.randrange(4,12),rng.randrange(9,18)) for _ in range(22)]
for i in range(48):
    a=2*math.pi*i/48; im,d=base(W,H)
    # side code field, behind the globe
    for j,(offset,speed,length) in enumerate(streams):
        x=594+j*14; head=(offset*13+i*speed)%420-40
        for k in range(length):
            y=head-k*14
            if 30<y<270:
                val='01ABCDEF'[(j*7+k*3+i//3)%8]; col='#163922' if k>2 else '#2b6537'; text(d,(x,y),val,10,col)
    d.rectangle((18,20,569,279),fill=BG)
    text(d,(34,25),'KENSHO // DEVELOPER PROFILE',12,GREEN,True)
    text(d,(886,25),'01 / IDENTITY',11,MUTED,anchor='ra')
    line(d,[(34,49),(886,49)],'#285038')
    text(d,(34,68),'$ whoami',14,TEAL)
    text(d,(30,92),'ALEXANDER',48,WHITE,True)
    text(d,(30,147),'ALCOCER_',48,GREEN,True)
    # cursor flash next to the name
    if i%12<7: d.rectangle((293,190,305,195),fill=GREEN)
    text(d,(35,212),'SOFTWARE DEVELOPMENT / LINUX / AUTOMATION',13,WHITE)
    text(d,(35,235),'AREQUIPA, PERU   |   TECSUP',12,MUTED)
    # projected wire globe
    cx,cy,r=743,161,88
    for radius in [103,115]:
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline='#285038')
    for q in range(0,360,15):
        ang=math.radians(q); line(d,[(cx+108*math.cos(ang),cy+108*math.sin(ang)),(cx+114*math.cos(ang),cy+114*math.sin(ang))],MUTED)
    def project(lat,lon):
        x=math.cos(lat)*math.cos(lon+a); y=math.sin(lat); z=math.cos(lat)*math.sin(lon+a)
        yy=y*.94-z*.342; zz=y*.342+z*.94
        return (cx+x*r,cy+yy*r,zz)
    for lat in [math.radians(x) for x in range(-75,76,15)]:
        for j in range(72):
            p=project(lat,j*math.tau/72); q=project(lat,(j+1)*math.tau/72)
            if p[2]>0 and q[2]>0: line(d,[p[:2],q[:2]],'#4f9954')
    for lon in [j*math.tau/12 for j in range(12)]:
        for j in range(30):
            p=project(-math.pi/2+j*math.pi/30,lon); q=project(-math.pi/2+(j+1)*math.pi/30,lon)
            if p[2]>0 and q[2]>0: line(d,[p[:2],q[:2]],'#35783f')
    for j in range(8):
        ang=a+j*math.tau/8; x=cx+110*math.cos(ang); y=cy+110*math.sin(ang); d.rectangle((x-2,y-2,x+2,y+2),fill=GREEN)
    text(d,(35,270),'[ PUBLIC PROFILE ]',10,GREEN); text(d,(886,270),'SYSTEM ONLINE',10,TEAL,anchor='ra'); corners(d,W,H)
    frames.append(im)
gif('identity.gif',frames,95); frames[8].save(OUT/'identity-preview.png')

# 02 — live terminal with typing and persistent completed information
frames=[]; W,H=920,176
cmds=[('python -m developer','Python / scripting / automation'),('uname -a','Linux: Kali | Debian | CentOS'),('git status','React / Node.js / Laravel / PHP'),('ls databases/','MongoDB / MySQL')]
for i in range(72):
    im,d=base(W,H); d.rectangle((10,10,W-11,H-11),fill=BG,outline='#285038');d.rectangle((11,11,W-12,36),fill=PANEL)
    for x,c in [(26,'#4c6d50'),(41,'#78974c'),(56,GREEN)]: d.ellipse((x,20,x+7,27),fill=c)
    text(d,(W//2,24),'kensho@profile:~',11,MUTED,anchor='mm');text(d,(W-25,24),'SHELL / 01',10,TEAL,anchor='rm')
    active=min(i//15,3); phase=i%15 if i<60 else 14
    for j,(cmd,out) in enumerate(cmds):
        y=48+j*27
        text(d,(26,y),'$',13,GREEN,True)
        if j<=active:
            typed=cmd if j<active else cmd[:min(len(cmd),int((phase+1)*len(cmd)/9))]
            text(d,(46,y),typed,13,WHITE)
            if j==active and phase<9 and i%4<2: text(d,(46+len(typed)*8,y),'_',13,GREEN)
            if j<active or phase>=9: text(d,(367,y),'[ OK ]',12,GREEN);text(d,(440,y),out,12,TEAL)
    frames.append(im)
gif('terminal.gif',frames,85)

# 03 — individually illustrated project GIFs; abstract representations, not app screenshots
projects=[('EDUMAP','EDTECH / DISCOVERY','map'),('DASH','MULTIMEDIA / PLAYER','audio'),('OASIS','NEURAL NETWORKS / WIP','net'),('SCREENANSWER','SOFTWARE / SIMPLICITY','scan')]
for idx,(name,tag,kind) in enumerate(projects):
    frames=[]; W,H=448,156
    for i in range(36):
        im,d=base(W,H); a=math.tau*i/36
        text(d,(17,15),f'PROJECT / 0{idx+1}',10,TEAL); text(d,(16,48),name,25,GREEN,True); text(d,(17,86),tag,10,WHITE)
        text(d,(17,132),'[ IN DEVELOPMENT ]' if kind=='net' else '[ PROJECT FILE ]',10,MUTED)
        line(d,[(260,13),(260,142)],'#285038')
        if kind=='map':
            for j in range(4):line(d,[(274,27+j*33),(430,17+j*33)],'#285038',2)
            for j in range(4):line(d,[(285+j*38,19),(275+j*38,141)],'#285038',2)
            pts=[(299,52),(375,40),(408,111),(330,120)]; line(d,pts,'#4c8954',2)
            for k,(x,y) in enumerate(pts):
                r=7+((i+k*8)%36)/36*16;d.ellipse((x-r,y-r,x+r,y+r),outline='#285b37');d.ellipse((x-4,y-4,x+4,y+4),fill=GREEN)
        elif kind=='audio':
            for j in range(25):
                x=276+j*6; ht=8+46*abs(math.sin(a*2+j*.51)*math.cos(a+j*.22)); col=GREEN if j%4 else TEAL; line(d,[(x,79-ht),(x,79+ht)],col,3)
            line(d,[(276,133),(425,133)],'#285038',2);line(d,[(276,133),(276+149*i/35,133)],GREEN,2)
        elif kind=='net':
            layers=[[(283,42),(283,79),(283,116)],[(330,30),(330,62),(330,95),(330,128)],[(377,42),(377,79),(377,116)],[(423,79)]]
            for j in range(3):
                for k,p in enumerate(layers[j]):
                    for l,q in enumerate(layers[j+1]):
                        line(d,[p,q],'#285038'); t=(i/36+j*.15+k*.12+l*.07)%1; x=p[0]+(q[0]-p[0])*t;y=p[1]+(q[1]-p[1])*t
                        if (k+l)%2==0:d.ellipse((x-1.5,y-1.5,x+1.5,y+1.5),fill=TEAL)
            for lay in layers:
                for x,y in lay:d.ellipse((x-4,y-4,x+4,y+4),fill=BG,outline=GREEN,width=2)
        else:
            d.rectangle((277,29,428,127),outline='#4f8356');d.rectangle((289,43,415,113),outline='#285038')
            for j in range(5):line(d,[(301,53+j*11),(400-(j%3)*17,53+j*11)],'#4a7e52',2)
            y=44+(i/35)*67;line(d,[(285,y),(420,y)],GREEN,2)
            for x,y,sx,sy in [(281,33,1,1),(424,33,-1,1),(281,123,1,-1),(424,123,-1,-1)]:line(d,[(x+sx*12,y),(x,y),(x,y+sy*12)],TEAL,2)
        corners(d,W,H);frames.append(im)
    gif(name.lower()+'.gif',frames,90)

# 04 — compact outro / animated scanline
frames=[]
for i in range(30):
    im,d=base(920,70); corners(d,920,70);text(d,(25,16),'$ exit',14,GREEN,True);text(d,(25,40),'SESSION CLOSED // SOURCE CODE NEVER SLEEPS.',12,WHITE)
    for j in range(24):d.rectangle((690+j*8,25,695+j*8,44),fill=GREEN if j<=i%24 else '#23412b')
    frames.append(im)
gif('outro.gif',frames,100)
