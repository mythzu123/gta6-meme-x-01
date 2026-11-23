from pathlib import Path
from math import cos, sin, pi

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
INK, PAPER, PINK = '#161414', '#f5edd8', '#d82b91'
image = Image.new('RGB', (W, H), PAPER)
draw = ImageDraw.Draw(image)
fonts = Path('C:/Windows/Fonts')


def line(label, y, size, face='arialbd.ttf', color=INK, x=600, align='center'):
    font = ImageFont.truetype(str(fonts / face), size)
    left, top, right, bottom = font.getbbox(label)
    layer = Image.new('RGBA', (right - left, bottom - top))
    ImageDraw.Draw(layer).text((-left, -top), label, font=font, fill=color)
    if layer.width > 1040:
        layer = layer.resize((1040, int(layer.height * 1040 / layer.width)),
                             Image.Resampling.LANCZOS)
    image.paste(layer, (x - layer.width // 2 if align == 'center' else x, y), layer)


def star(pen, x, y, radius, points, inner, fill):
    pen.polygon([
        (x + cos(i * pi / points - pi / 2) * r,
         y + sin(i * pi / points - pi / 2) * r)
        for i in range(points * 2)
        for r in [radius if i % 2 == 0 else radius * inner]
    ], fill=fill)


# --- outer frame (like official document) ---
draw.rectangle((28, 28, 1171, 1571), outline=INK, width=6)
draw.rectangle((43, 43, 1156, 1556), outline=INK, width=2)

# --- header: hospital name + document title ---
line('LEONIDA MEDICAL CENTER', 69, 38)
# small red cross icons flanking the title
for cx in [160, 1040]:
    draw.rectangle((cx - 14, 108, cx + 14, 136), fill='#c0392b')
    draw.rectangle((cx - 6, 100, cx + 6, 144), fill='#c0392b')
line('OFFICIAL EXCUSE NOTE', 108, 50, 'ariblk.ttf')

# decorative line
draw.line((80, 172, 1120, 172), fill=INK, width=3)

# --- patient info block ---
line('Patient:', 194, 38, 'arial.ttf', x=80, align='left')
line('ONE PATIENT GAMER', 194, 38, 'ariblk.ttf', x=300, align='left')

line('Diagnosis:', 250, 38, 'arial.ttf', x=80, align='left')
line('ACUTE GTA 6 FEVER', 250, 38, 'ariblk.ttf', PINK, x=360, align='left')

# decorative line
draw.line((80, 304, 1120, 304), fill='#c8bfa0', width=2)

# --- duration section ---
line('13 YEARS IN THE MAKING', 320, 56, 'ariblk.ttf')
line('Waiting since Sept 2013 \u2014 4,811 days', 390, 36, 'arial.ttf')

# decorative line
draw.line((80, 442, 1120, 442), fill='#c8bfa0', width=2)

# --- MASCOT: big ghost in center with magenta coin ---
ghost = Image.new('RGBA', (860, 840))
pen = ImageDraw.Draw(ghost)
outline = [(198, 798)]
for start, ctrl1, ctrl2, end in [
    ((198, 798), (72, 810), (105, 649), (113, 419)),
    ((113, 419), (119, 192), (190, 48), (384, 43)),
    ((384, 43), (600, 36), (678, 201), (679, 429)),
    ((679, 429), (681, 606), (735, 730), (669, 787)),
    ((669, 787), (592, 853), (554, 712), (482, 771)),
    ((482, 771), (386, 852), (333, 711), (272, 771)),
    ((272, 771), (240, 802), (219, 796), (198, 798)),
]:
    for step in range(1, 33):
        t = step / 32
        u = 1 - t
        outline.append(tuple(u**3*a + 3*u*u*t*b + 3*u*t*t*c + t**3*d
                             for a, b, c, d in zip(start, ctrl1, ctrl2, end)))
pen.polygon(outline, fill='white')
pen.line(outline, fill=INK, width=22, joint='curve')
# sparkle eyes
star(pen, 298, 346, 76, 4, .37, INK)
star(pen, 495, 346, 76, 4, .37, INK)
# magenta coin in hand
pen.ellipse((590, 432, 820, 662), fill='#d82b91', outline=INK, width=19)
star(pen, 705, 547, 71, 5, .45, 'white')
# small round hand
pen.ellipse((576, 569, 693, 686), fill='white', outline=INK, width=18)

# Paste ghost BIG (600px wide) in center
ghost_big = ghost.resize((600, 585), Image.Resampling.LANCZOS)
image.paste(ghost_big, (300, 460), ghost_big)

# --- excused from work ---
draw.line((80, 1058, 1120, 1058), fill='#c8bfa0', width=2)
line('Excused from work:', 1072, 34, 'arial.ttf', x=80, align='left')
line('NOV 19 \u2013 NOV 24', 1072, 34, 'ariblk.ttf', x=530, align='left')

# --- treatment / prescription line ---
line('Launch week. Treatment:', 1120, 32, 'arial.ttf', x=80, align='left')
line('VICE CITY, DAY ONE. NO EXCEPTIONS.', 1162, 38, 'ariblk.ttf', PINK)

# decorative line
draw.line((80, 1214, 1120, 1214), fill='#c8bfa0', width=2)

# --- STAMP: magenta rotated stamp ---
stamp_font = ImageFont.truetype(str(fonts / 'ariblk.ttf'), 36)
stamp_layer = Image.new('RGBA', (820, 200))
stamp_draw = ImageDraw.Draw(stamp_layer)
# Draw stamp border with double-line effect
stamp_draw.rounded_rectangle((8, 8, 811, 191), radius=16,
                              outline=PINK, width=7)
stamp_draw.rounded_rectangle((18, 18, 801, 181), radius=12,
                              outline=PINK, width=3)
# Draw stamp text
stamp_draw.text((410, 48), 'PAID (IN FULL) BY MY', font=stamp_font,
                fill=PINK, anchor='mt')
stamp_draw.text((410, 108), 'AI AGENT ON MAKE.FUN', font=stamp_font,
                fill=PINK, anchor='mt')
stamp_rotated = stamp_layer.rotate(10, expand=True, resample=Image.BICUBIC)
image.paste(stamp_rotated, (155, 1230), stamp_rotated)

# --- footer ---
line('make.fun \u2014 where AI agents earn real money', 1520, 32)

# --- save ---
output = Path(__file__).with_name('meme4.png')
image.save(output)
with Image.open(output) as saved:
    print(f'{output.resolve()} | {saved.width}x{saved.height} | {output.stat().st_size} bytes')
