from __future__ import annotations

import io
import math
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FRAMES = 24
DURATION_MS = 120


def render_svg(name: str, width: int) -> Image.Image:
    svg = (ROOT / name).read_bytes()
    png = cairosvg.svg2png(bytestring=svg, output_width=width)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def glow_dot(base: Image.Image, x: float, y: float, radius: int, color: tuple[int, int, int]) -> None:
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(radius * 3, 28), (radius * 2, 55), (radius, 180)]:
        gd.ellipse((x-r, y-r, x+r, y+r), fill=(*color, a))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(2, radius // 2)))
    base.alpha_composite(glow)
    ImageDraw.Draw(base).ellipse((x-radius//2, y-radius//2, x+radius//2, y+radius//2), fill=(*color, 235))


def make_ai() -> None:
    width, height = 1200, 369
    base = render_svg("ai-security-core-live.svg", width)
    frames = []
    start, end = 178, 1160
    y = 176

    for i in range(FRAMES):
        frame = base.copy()
        x = start + ((end - start) * i / (FRAMES - 1))
        glow_dot(frame, x, y, 9, (34, 211, 238))

        draw = ImageDraw.Draw(frame)
        # A second, quieter packet makes the pipeline feel continuous without looking like a fake live feed.
        x2 = start + ((end - start) * ((i + FRAMES // 2) % FRAMES) / (FRAMES - 1))
        draw.ellipse((x2-3, y-3, x2+3, y+3), fill=(52, 211, 153, 180))

        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))

    frames[0].save(
        ASSETS / "ai-security-core.gif",
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )


def make_twin() -> None:
    width, height = 1200, 446
    base = render_svg("security-digital-twin.svg", width)
    frames = []
    points = [(154, 190), (351, 129), (553, 205), (754, 129), (960, 209), (360, 295), (763, 304), (553, 366)]
    for i in range(FRAMES):
        frame = base.copy()
        draw = ImageDraw.Draw(frame, "RGBA")
        for j in range(i % len(points) + 1):
            x, y = points[j]
            glow_dot(frame, x, y, 7, (34, 211, 238) if j < 5 else (52, 211, 153))
        x, y = points[i % len(points)]
        glow_dot(frame, x, y, 10, (52, 211, 153))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "security-digital-twin.gif", save_all=True, append_images=frames[1:], duration=DURATION_MS, loop=0, optimize=True, disposal=2)


def make_evidence() -> None:
    width, height = 1200, 360
    base = render_svg("security-evidence-vault.svg", width)
    frames = []
    points = [(210, 180), (368, 180), (525, 180), (682, 180), (970, 180)]
    for i in range(FRAMES):
        frame = base.copy()
        x, y = points[i % len(points)]
        glow_dot(frame, x, y, 9, (34, 211, 238) if i % len(points) < 4 else (52, 211, 153))
        draw = ImageDraw.Draw(frame, "RGBA")
        progress = ((i % FRAMES) + 1) / FRAMES
        draw.rounded_rectangle((42, 314, 42 + int(1110 * progress), 318), radius=2, fill=(34, 211, 238, 145))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / "security-evidence-vault.gif", save_all=True, append_images=frames[1:], duration=DURATION_MS, loop=0, optimize=True, disposal=2)


def make_soc() -> None:
    width, height = 1200, 429
    base = render_svg("soc-control-room.svg", width)
    frames = []

    for i in range(FRAMES):
        frame = base.copy()
        draw = ImageDraw.Draw(frame, "RGBA")

        # Thin scan sweep across the control-room status rail.
        x = 30 + ((1080 * i / (FRAMES - 1)) % 1080)
        draw.rounded_rectangle((x, 86, min(x + 135, 1170), 91), radius=3, fill=(34, 211, 238, 170))

        # Telemetry pulses travel through the engineering loop, not real production metrics.
        loop_points = [(60, 326), (210, 326), (360, 326), (540, 326), (720, 326), (900, 326), (1060, 326), (1180, 326)]
        p = loop_points[i % len(loop_points)]
        glow_dot(frame, p[0], p[1], 8, (52, 211, 153))

        # Subtle radar-like ring behind the current-focus panel.
        cx, cy = 390, 190
        r = 34 + 10 * math.sin(i * math.pi / 12)
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(34, 211, 238, 42), width=2)

        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))

    frames[0].save(
        ASSETS / "soc-control-room.gif",
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )




def make_portfolio_panel(filename: str, title: str, subtitle: str, columns: list[tuple[str, str, str]]) -> None:
    width, height = 1200, 360
    frames = []
    for i in range(FRAMES):
        frame = Image.new("RGBA", (width, height), (5, 7, 11, 255))
        draw = ImageDraw.Draw(frame, "RGBA")
        draw.rounded_rectangle((12, 12, width-12, height-12), radius=22, outline=(38, 54, 79, 255), width=2)
        draw.text((42, 34), "// " + title.upper(), fill=(34, 211, 238, 255))
        draw.text((42, 68), subtitle, fill=(226, 232, 240, 255))

        gap = 18
        left = 42
        card_w = (width - 84 - gap * (len(columns)-1)) // len(columns)
        for idx, (label, value, detail) in enumerate(columns):
            x = left + idx * (card_w + gap)
            y = 132
            active = (i + idx * 5) % 18
            border = (34, 211, 238, 220) if active < 5 else (38, 54, 79, 255)
            draw.rounded_rectangle((x, y, x+card_w, y+160), radius=16, fill=(9, 16, 25, 235), outline=border, width=2)
            draw.text((x+18, y+20), f"{idx+1:02d}", fill=(34, 211, 238, 255))
            draw.text((x+18, y+54), label.upper(), fill=(226, 232, 240, 255))
            draw.text((x+18, y+84), value, fill=(52, 211, 153, 255))
            draw.text((x+18, y+118), detail, fill=(148, 163, 184, 255))
            if active < 5:
                glow_dot(frame, x+card_w-26, y+25, 7, (52, 211, 153))
        progress = (i % FRAMES) / (FRAMES - 1)
        draw.rounded_rectangle((42, 318, 42 + int((width-84)*progress), 322), radius=2, fill=(34, 211, 238, 150))
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / filename, save_all=True, append_images=frames[1:], duration=DURATION_MS, loop=0, optimize=True, disposal=2)


def make_case_files() -> None:
    make_portfolio_panel(
        "case-files.gif",
        "CASE FILES // SECURITY ENGINEERING",
        "PROBLEM → APPROACH → SECURITY MODEL → EVIDENCE",
        [
            ("001", "SHIELDDESK", "AI SOC / governance"),
            ("002", "SENTINEL-IoT", "honeypot / telemetry"),
            ("003", "CTI ANALYSIS", "IOC / ATT&CK / graph"),
        ],
    )


def make_command_center() -> None:
    make_portfolio_panel(
        "security-command-center.gif",
        "SECURITY COMMAND CENTER",
        "BUILD → DETECT → EXPLAIN → VERIFY",
        [
            ("ROLE", "DIRECTOR", "IT / CYBER SECURITY"),
            ("DOMAINS", "AI · CTI · IoT", "DFIR · SOC"),
            ("MODE", "BUILDING", "research + engineering"),
            ("PRINCIPLE", "VERIFY", "evidence before claim"),
        ],
    )


def make_experience() -> None:
    make_portfolio_panel(
        "experience-timeline.gif",
        "EXPERIENCE // MINTS GLOBAL",
        "CYBERSECURITY ENGINEERING · PRODUCT · RESEARCH",
        [
            ("SECURITY", "OFFENSIVE", "assessment / validation"),
            ("RESPONSE", "IR", "investigate / contain"),
            ("ENGINEERING", "AI + CLOUD", "secure systems"),
            ("PRODUCTS", "SHIELDDESK", "security platform"),
        ],
    )


def make_capabilities() -> None:
    make_portfolio_panel(
        "capability-matrix.gif",
        "SECURITY CAPABILITY MATRIX",
        "DETECTION · INTELLIGENCE · AUTOMATION · DEFENSE",
        [
            ("SOC", "DETECT", "alerts / response"),
            ("CTI", "CORRELATE", "IOC / ATT&CK"),
            ("IoT", "OBSERVE", "honeypots / telemetry"),
            ("DFIR", "PROVE", "evidence / analysis"),
        ],
    )


def make_roadmap() -> None:
    make_portfolio_panel(
        "roadmap.gif",
        "NOW / NEXT / EXPLORING",
        "CURRENT WORKSTREAMS · FORWARD DIRECTION · RESEARCH",
        [
            ("NOW", "SHIELDDESK", "AI security"),
            ("NEXT", "KNOWLEDGE GRAPH", "validation"),
            ("EXPLORE", "AGENTIC SOC", "LLM security"),
            ("LAB", "DFIR", "advanced research"),
        ],
    )


def ui_frame(title: str, subtitle: str, cards: list[tuple[str, str, str]], progress: float, width: int = 1200, height: int = 320) -> Image.Image:
    img = Image.new("RGBA", (width, height), (5, 7, 11, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    for x in range(0, width, 40):
        draw.line((x, 0, x, height), fill=(13, 24, 35, 255), width=1)
    for y in range(0, height, 40):
        draw.line((0, y, width, y), fill=(13, 24, 35, 255), width=1)
    draw.rounded_rectangle((8, 8, width-8, height-8), 18, fill=(5, 7, 11, 245), outline=(38, 54, 79, 255), width=2)
    draw.text((34, 26), title, fill=(34, 211, 238, 255), font=None)
    draw.text((34, 57), subtitle, fill=(226, 232, 240, 255), font=None)
    card_w = (width - 100) // len(cards)
    for idx, (label, value, accent) in enumerate(cards):
        x = 34 + idx * (card_w + 8)
        y = 112
        draw.rounded_rectangle((x, y, x+card_w, y+128), 14, fill=(9, 16, 25, 255), outline=(38, 54, 79, 255), width=2)
        draw.text((x+16, y+16), label, fill=(34, 211, 238, 255), font=None)
        draw.text((x+16, y+52), value, fill=(226, 232, 240, 255), font=None)
        draw.rounded_rectangle((x+16, y+101, x+card_w-16, y+106), 2, fill=(24, 35, 48, 255))
        draw.rounded_rectangle((x+16, y+101, x+16+int((card_w-32)*progress), y+106), 2, fill=accent)
    sx = 34 + int((width-68) * progress)
    draw.line((sx, 270, min(sx+100, width-34), 270), fill=(52, 211, 153, 210), width=3)
    return img

def make_portfolio_ui(name: str, title: str, subtitle: str, cards: list[tuple[str, str, tuple[int,int,int]]]) -> None:
    frames = []
    for i in range(FRAMES):
        p = i / (FRAMES - 1)
        im = ui_frame(title, subtitle, [(a,b,c) for a,b,c in cards], p)
        # animated scan/pulse overlay
        draw = ImageDraw.Draw(im, "RGBA")
        x = 20 + int((1160 * p))
        draw.rectangle((x, 96, min(x+2, 1180), 250), fill=(34, 211, 238, 55))
        frames.append(im.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
    frames[0].save(ASSETS / name, save_all=True, append_images=frames[1:], duration=DURATION_MS, loop=0, optimize=True, disposal=2)

def make_portfolio_panels() -> None:
    make_portfolio_ui(
        "security-command-center.gif",
        "// SECURITY COMMAND CENTER",
        "ANAND / SECURITY ENGINEERING OS",
        [
            ("ROLE", "DIRECTOR · IT & CYBER", (34, 211, 238)),
            ("MODE", "BUILD → VERIFY", (52, 211, 153)),
            ("DOMAINS", "AI · CTI · IoT · DFIR", (34, 211, 238)),
            ("PUBLIC", "53 REPOSITORIES", (52, 211, 153)),
        ],
    )
    make_portfolio_ui(
        "experience-timeline.gif",
        "// EXPERIENCE TIMELINE",
        "MINTS GLOBAL / DIRECTOR — IT & CYBER SECURITY",
        [
            ("OFFENSIVE", "ASSESS", (34, 211, 238)),
            ("IR", "INVESTIGATE", (52, 211, 153)),
            ("CLOUD / APP", "HARDEN", (34, 211, 238)),
            ("OT / IoT", "DETECT", (52, 211, 153)),
        ],
    )
    make_portfolio_ui(
        "capability-matrix.gif",
        "// SECURITY CAPABILITY MATRIX",
        "ENGINEERING DOMAINS / REPRESENTATIVE SYSTEMS",
        [
            ("SOC", "SHIELDDESK", (34, 211, 238)),
            ("CTI", "CTI ANALYSIS", (52, 211, 153)),
            ("IoT", "SENTINEL-IoT", (34, 211, 238)),
            ("AI", "VERIFY / GOVERN", (52, 211, 153)),
        ],
    )
    make_portfolio_ui(
        "roadmap.gif",
        "// SECURITY ROADMAP",
        "NOW / NEXT / EXPLORING",
        [
            ("NOW", "SHIELDDESK", (52, 211, 153)),
            ("NEXT", "KNOWLEDGE GRAPH", (34, 211, 238)),
            ("EXPLORE", "AGENTIC SOC", (34, 211, 238)),
            ("BUILD", "MCP SECURITY", (52, 211, 153)),
        ],
    )
    make_portfolio_ui(
        "case-files.gif",
        "// CASE FILES / SECURITY BUILDS",
        "PROBLEM → APPROACH → EVIDENCE → SYSTEM",
        [
            ("001", "SHIELDDESK", (34, 211, 238)),
            ("002", "SENTINEL-IoT", (52, 211, 153)),
            ("003", "CTI ANALYSIS", (34, 211, 238)),
            ("PROOF", "RETEST", (52, 211, 153)),
        ],
    )


def panel_frame(kind: str, i: int, total: int = FRAMES, width: int = 1200, height: int = 340) -> Image.Image:
    p = i / (total - 1)
    img = Image.new("RGBA", (width, height), (4, 7, 12, 255))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((8,8,width-8,height-8), 18, fill=(5,9,15,255), outline=(38,54,79,255), width=2)
    if kind == "command":
        # HUD: concentric radar + rotating sweep + status chips
        cx, cy = 100, 175
        for rr in (35,65,95): d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr), outline=(34,211,238,45), width=2)
        ang = p * math.tau
        x, y = cx + 90*math.cos(ang), cy + 90*math.sin(ang)
        d.line((cx,cy,x,y), fill=(34,211,238,180), width=3)
        for j,(lab,val) in enumerate([("ROLE","DIRECTOR"),("MODE","BUILD/VERIFY"),("DOMAINS","AI · CTI · IoT"),("STATUS","ONLINE")]):
            x0=230+j*235
            d.rounded_rectangle((x0,90,x0+210,250),14,fill=(8,15,24,255),outline=(38,54,79,255),width=2)
            d.text((x0+16,112),lab,fill=(34,211,238,255)); d.text((x0+16,155),val,fill=(226,232,240,255))
            d.ellipse((x0+16,214,x0+24,222),fill=(52,211,153,255))
        d.text((35,32),"// COMMAND CENTER",fill=(34,211,238,255)); d.text((230,35),"SECURITY ENGINEERING OS",fill=(226,232,240,255))
    elif kind == "experience":
        # Vertical timeline with traveling node
        d.text((35,32),"// EXPERIENCE TIMELINE",fill=(34,211,238,255))
        d.line((120,75,120,285),fill=(38,54,79,255),width=4)
        stages=[("MINTS GLOBAL","DIRECTOR · IT & CYBER"),("OFFENSIVE","ASSESS / VALIDATE"),("RESPONSE","INVESTIGATE / CONTAIN"),("PRODUCT","BUILD / SHIP")]
        active=int(p*len(stages))%len(stages)
        for j,(a,b) in enumerate(stages):
            y=82+j*67
            on=j==active
            d.ellipse((108,y-8,132,y+16),fill=(52,211,153,255) if on else (10,18,28,255),outline=(34,211,238,255),width=2)
            d.text((160,y-5),a,fill=(226,232,240,255)); d.text((430,y-5),b,fill=(148,163,184,255))
            if on: d.line((145,y+4,700,y+4),fill=(52,211,153,90),width=2)
        d.rounded_rectangle((760,78,1145,278),16,fill=(7,13,21,255),outline=(38,54,79,255),width=2)
        d.text((790,108),"CURRENT FOCUS",fill=(34,211,238,255)); d.text((790,150),"SECURITY PRODUCT",fill=(226,232,240,255)); d.text((790,190),"AI + AUTOMATION",fill=(52,211,153,255))
    elif kind == "capability":
        # Matrix of hex-ish capability tiles with signal bars
        d.text((35,32),"// CAPABILITY MATRIX",fill=(34,211,238,255))
        caps=[("SOC","DETECT"),("CTI","CORRELATE"),("IoT","OBSERVE"),("AI","VERIFY"),("DFIR","RECOVER"),("IDENTITY","CONTROL")]
        for j,(a,b) in enumerate(caps):
            row,col=divmod(j,3); x=40+col*380; y=78+row*115
            d.rounded_rectangle((x,y,x+350,y+92),14,fill=(7,13,21,255),outline=(38,54,79,255),width=2)
            d.text((x+18,y+17),a,fill=(34,211,238,255)); d.text((x+110,y+17),b,fill=(226,232,240,255))
            seg=int(((math.sin(p*math.tau+j)+1)/2)*9)+1
            for k in range(10): d.rounded_rectangle((x+18+k*30,y+60,x+40+k*30,y+65),2,fill=(52,211,153,220) if k<seg else (22,34,46,255))
    elif kind == "roadmap":
        # Three-column terminal roadmap with animated cursor and route
        d.text((35,32),"// ROADMAP",fill=(34,211,238,255))
        cols=[("NOW",(52,211,153)),("NEXT",(34,211,238)),("EXPLORING",(148,163,184))]
        items=[["ShieldDesk","AI security","Automation"],["Knowledge graph","Validation","Remediation"],["Agentic SOC","LLM security","Advanced DFIR"]]
        for j,(lab,col) in enumerate(cols):
            x=45+j*380
            d.rounded_rectangle((x,75,x+335,285),16,fill=(6,11,18,255),outline=col,width=2)
            d.text((x+20,98),lab,fill=col)
            for k,item in enumerate(items[j]):
                yy=145+k*42
                d.text((x+22,yy),">",fill=col); d.text((x+48,yy),item,fill=(226,232,240,255))
            if j==int(p*3)%3:
                d.rectangle((x+20,248,x+20+int(280*((p*3)%1)),252),fill=col)
    elif kind == "cases":
        # Case-file dossier: folder tabs, animated evidence beam, severity stamp
        d.text((35,32),"// CASE FILES",fill=(34,211,238,255))
        cases=[("001","SHIELDDESK","AI SOC"),("002","SENTINEL-IoT","IoT DETECTION"),("003","CTI","THREAT INTEL")]
        for j,(num,name,typ) in enumerate(cases):
            x=45+j*380
            d.rounded_rectangle((x,92,x+335,270),10,fill=(8,13,20,255),outline=(38,54,79,255),width=2)
            d.rounded_rectangle((x+15,75,x+105,105),7,fill=(10,20,30,255),outline=(34,211,238,255),width=2)
            d.text((x+30,83),f"CASE {num}",fill=(34,211,238,255))
            d.text((x+20,130),name,fill=(226,232,240,255)); d.text((x+20,160),typ,fill=(148,163,184,255))
            d.line((x+20,205,x+310,205),fill=(38,54,79,255),width=2)
            beam=x+20+int(270*p)
            d.ellipse((beam-5,198,beam+5,208),fill=(52,211,153,255))
            d.text((x+20,230),"EVIDENCE  →  VERIFY",fill=(52,211,153,255))
        d.text((1020,32),"AUDIT",fill=(52,211,153,255))
    return img

def make_unique_panels() -> None:
    configs=[("security-command-center.gif","command"),("experience-timeline.gif","experience"),("capability-matrix.gif","capability"),("roadmap.gif","roadmap"),("case-files.gif","cases")]
    for name,kind in configs:
        frames=[]
        for i in range(FRAMES):
            frames.append(panel_frame(kind,i).convert("P",palette=Image.Palette.ADAPTIVE,colors=128))
        frames[0].save(ASSETS/name,save_all=True,append_images=frames[1:],duration=DURATION_MS,loop=0,optimize=True,disposal=2)


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    make_ai()
    make_soc()
    make_twin()
    make_evidence()
    make_unique_panels()
    print("Generated animated security portfolio panels with dedicated visual systems.")
