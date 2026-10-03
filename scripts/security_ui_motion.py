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


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    make_ai()
    make_soc()
    make_twin()
    make_evidence()
    make_case_files()
    make_command_center()
    make_experience()
    make_capabilities()
    make_roadmap()
    print("Generated animated security portfolio panels.")
