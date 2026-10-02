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


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    make_ai()
    make_soc()
    print("Generated AI Security Core and SOC Control Room GIFs.")
