from pathlib import Path
from math import cos, sin, pi

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
INK, PAPER, PINK = '#161414', '#f5edd8', '#b91b73'
image = Image.new('RGB', (W, H), PAPER)
draw = ImageDraw.Draw(image)
fonts = Path('C:/Windows/Fonts')


def line(label, y, size, face='arialbd.ttf', color=INK, x=600, align='center'):
    font = ImageFont.truetype(str(fonts / face), size)
    left, top, right, bottom = font.getbbox(label)
    layer = Image.new('RGBA', (right - left, bottom - top))
    ImageDraw.Draw(layer).text((-left, -top), label, font=font, fill=color)
    if layer.width > 1040:
        layer = layer.resize((1040, layer.height), Image.Resampling.LANCZOS)
    image.paste(layer, (x - layer.width // 2 if align == 'center' else x, y), layer)


def star(pen, x, y, radius, points, inner, fill):
    pen.polygon([
        (x + cos(i * pi / points - pi / 2) * r,
         y + sin(i * pi / points - pi / 2) * r)
        for i in range(points * 2)
        for r in [radius if i % 2 == 0 else radius * inner]
    ], fill=fill)


draw.rectangle((28, 28, 1171, 1571), outline=INK, width=6)
draw.rectangle((43, 43, 1156, 1556), outline=INK, width=2)
line(' '.join("LEONIDA COUNTY SHERIFF'S OFFICE"), 69, 27)
for x in range(464, 737, 68):
    star(draw, x, 137, 26, 5, .46, PINK)
line('WANTED', 176, 190, 'ariblk.ttf')
line('FOR GRAND THEFT PATIENCE', 332, 51)

draw.rectangle((75, 402, 1125, 915), fill='#e1e0dc')
for y in range(443, 890, 54):
    draw.line((76, y, 1124, y), fill='#a7a6a1', width=2)
for y, label in [(443, "6'0\""), (605, "5'6\""), (767, "5'0\"")]:
    draw.line((76, y, 1124, y), fill='#777672', width=4)
    draw.rectangle((90, y - 20, 177, y + 20), fill='#e1e0dc')
    line(label, y - 12, 29, x=132)

# Draw the mascot at double resolution so the curved outline stays smooth.
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
star(pen, 298, 346, 76, 4, .37, INK)
star(pen, 495, 346, 76, 4, .37, INK)
pen.ellipse((590, 432, 820, 662), fill='#d82b91', outline=INK, width=19)
star(pen, 705, 547, 71, 5, .45, 'white')
pen.ellipse((576, 569, 693, 686), fill='white', outline=INK, width=18)
ghost = ghost.resize((470, 459), Image.Resampling.LANCZOS)
image.paste(ghost, (365, 424), ghost)
draw.rectangle((75, 402, 1125, 915), outline=INK, width=5)

draw.rectangle((75, 916, 1125, 975), fill=INK)
line('ONE PATIENT GAMER — IN LINE SINCE SEPT 2013', 934, 37, color='white')
line('CHARGES:', 997, 32, 'ariblk.ttf', x=80, align='left')
charges = [
    'Waited 13 years in the release queue — 4,811 days',
    'Faked 5 sick days for launch week (doctor approved)',
    'Deleted the family photos to fit a 214 GB download',
    'Watched Trailer 2 a total of 87 times',
    'Survived Delay No. 1 and Delay No. 2',
]
for number, charge in enumerate(charges, 1):
    line(f'{number}. {charge}', 1042 + (number - 1) * 51, 40,
         'arial.ttf', x=80, align='left')

draw.rectangle((75, 1311, 1125, 1464), fill=INK)
line('REWARD PAID BY MY AI AGENT', 1333, 54, 'ariblk.ttf', 'white')
line('earned on make.fun while I did the waiting', 1401, 42, color='#ff72be')
line('make.fun — where AI agents earn real money', 1492, 32)

output = Path(__file__).with_name('meme2.png')
image.save(output)
with Image.open(output) as saved:
    print(f'{output.resolve()} | {saved.width}x{saved.height} | {output.stat().st_size} bytes')
