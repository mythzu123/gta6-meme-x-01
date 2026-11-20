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
line('13 YEARS IN THE QUEUE', 145, 94, 'ariblk.ttf')
for x, year in [(65, '2013'), (695, '2026')]:
    draw.rectangle((x, 345, x + 440, 1080), fill='#ede2c8', outline=INK, width=5)
    draw.rectangle((x, 345, x + 440, 480), fill=INK)
    line(year, 372, 104, 'ariblk.ttf', PAPER, x + 220)

draw.polygon([(525, 713), (628, 713), (628, 676), (680, 748),
              (628, 820), (628, 783), (525, 783)], fill=PINK)
line('13 YEARS', 642, 28)
line('LATER', 674, 28)

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
young = ghost.copy()
yp = ImageDraw.Draw(young)
yp.rounded_rectangle((10, 474, 335, 625), radius=18, fill=PAPER, outline=INK, width=15)
yp.text((172, 549), 'GTA 6 SOON!', font=ImageFont.truetype(str(fonts / 'arialbd.ttf'), 47),
        fill=INK, anchor='mm')
yp.ellipse((275, 592, 356, 668), fill='white', outline=INK, width=15)

old = ghost.rotate(-9, resample=Image.Resampling.BICUBIC)
op = ImageDraw.Draw(old)
# The walking stick sits behind the free hand; the coin remains visible.
op.line((139, 567, 64, 821), fill=INK, width=33)
op.line((139, 567, 64, 821), fill='#936a46', width=17)
op.polygon([(242, 422), (299, 450), (371, 423), (440, 455), (490, 432),
            (480, 553), (433, 643), (341, 727), (280, 662), (248, 557)],
           fill='white', outline=INK, width=14)
op.arc((304, 479, 435, 666), 55, 126, fill='#b6adaa', width=10)
op.ellipse((209, 235, 387, 413), outline=INK, width=20)
op.ellipse((409, 266, 587, 444), outline=INK, width=20)
op.line((384, 322, 414, 327), fill=INK, width=17)
op.ellipse((108, 530, 203, 619), fill='white', outline=INK, width=17)

for sprite, x in [(young, 75), (old, 705)]:
    sprite = sprite.resize((420, 410), Image.Resampling.LANCZOS)
    image.paste(sprite, (x, 551), sprite)

line('Day 1 in line. Full of hope.', 1121, 34, x=285)
line('Day 4,811. Still in line.', 1121, 34, x=915)
draw.rectangle((65, 1250, 1135, 1456), fill=INK)
line('MY AI AGENT EARNED REAL MONEY ON MAKE.FUN —', 1297, 41, color='white')
line('while I aged 13 years in this queue', 1372, 45, color='#ff72be')
line('make.fun — where AI agents earn real money', 1490, 34)

output = Path(__file__).with_name('meme3.png')
image.save(output)
with Image.open(output) as saved:
    print(f'{output.resolve()} | {saved.width}x{saved.height} | {output.stat().st_size} bytes')
