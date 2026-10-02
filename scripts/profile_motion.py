from PIL import Image, ImageDraw, ImageFont
import math, os

W,H=1200,430
frames=[]
font_b="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_m="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
fb=ImageFont.truetype(font_b,52)
fm=ImageFont.truetype(font_m,16)
fs=ImageFont.truetype(font_m,12)
roles=["AI × SECURITY","THREAT INTELLIGENCE","IoT / EMBEDDED SECURITY","DIGITAL FORENSICS"]
for i in range(32):
    im=Image.new("RGB",(W,H),(5,7,11)); d=ImageDraw.Draw(im)
    # grid
    for x in range(0,W,32): d.line((x,0,x,H),fill=(20,29,42),width=1)
    for y in range(0,H,32): d.line((0,y,W,y),fill=(20,29,42),width=1)
    # frame
    d.rounded_rectangle((2,2,W-3,H-3),28,outline=(34,211,238),width=2)
    # animated scan
    sy=(i*18)%H
    d.line((0,sy,W,sy),fill=(34,211,238),width=2)
    # radar
    cx,cy=255,215
    for r,c in [(105,(34,211,238)),(78,(139,92,246)),(52,(52,211,153))]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=c,width=1)
    ang=i*math.pi/16
    x2=cx+105*math.cos(ang); y2=cy+105*math.sin(ang)
    d.line((cx,cy,x2,y2),fill=(52,211,153),width=2)
    d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=(34,211,238))
    # left terminal
    d.rounded_rectangle((24,50,489,380),24,fill=(7,16,24),outline=(34,211,238),width=1)
    d.text((55,82),"SECURITY_PROFILE // LIVE",font=fs,fill=(148,163,184))
    d.text((55,315),"ANAND.BINU.ARJUN",font=fs,fill=(226,232,240))
    d.text((340,315),"PROFILE OS",font=fs,fill=(34,211,238))
    d.rectangle((55,350,445,352),fill=(30,41,59))
    d.rectangle((55,350,55+(i%21)*19,352),fill=(34,211,238))
    # right identity
    d.rounded_rectangle((535,52,1165,94),21,fill=(15,23,42),outline=(34,211,238))
    d.ellipse((554,67,566,79),fill=(52,211,153))
    d.text((576,61),"OPEN TO SECURITY COLLABORATIONS",font=fm,fill=(203,213,225))
    d.text((535,125),"> hello, I'm",font=fm,fill=(148,163,184))
    d.text((535,155),"ANAND BINU ARJUN",font=fb,fill=(34,211,238))
    role=roles[(i//8)%len(roles)]
    d.text((538,225),role,font=fm,fill=(34,211,238))
    d.text((538,270),"Building security systems that detect, explain and verify risk.",font=fm,fill=(148,163,184))
    cards=[("LOCATION","UNITED KINGDOM"),("FOCUS","AI / CYBER / IoT"),("STATUS","BUILDING SECURITY SYSTEMS")]
    xs=[535,738,941]; ws=[190,190,225]
    for (label,val),x,w in zip(cards,xs,ws):
        d.rounded_rectangle((x,334,x+w,376),12,fill=(11,18,32),outline=(51,65,85))
        d.text((x+17,340),label,font=fs,fill=(100,116,139))
        d.text((x+17,358),val,font=fs,fill=(226,232,240))
    frames.append(im)
os.makedirs("assets",exist_ok=True)
frames[0].save("assets/profile-motion.gif",save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True)
