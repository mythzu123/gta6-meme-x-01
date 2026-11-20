from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 1600
FONT_DIR = Path('C:/Windows/Fonts')
PAPER = '#f7f1de'
INK = '#29241f'


def font(size, style='regular'):
    names = {'regular': 'georgia.ttf', 'bold': 'georgiab.ttf', 'italic': 'georgiai.ttf'}
    return ImageFont.truetype(str(FONT_DIR / names[style]), size)


page = Image.new('RGB', (WIDTH, HEIGHT), PAPER)
draw = ImageDraw.Draw(page)
draw.rectangle((45, 45, 1154, 1554), outline=INK, width=4)
draw.rectangle((59, 59, 1140, 1540), outline=INK, width=2)


def centered(text, y, face):
    draw.text((WIDTH / 2, y), text, font=face, fill=INK, anchor='mt')


def paragraph(text, y, face, max_width=950, spacing=13):
    lines = []
    line = ''
    for word in text.split():
        candidate = f'{line} {word}'.strip()
        if draw.textlength(candidate, font=face) <= max_width:
            line = candidate
        else:
            if not line:
                raise ValueError('A word exceeds the available width')
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    advance = face.size + spacing
    for line in lines:
        draw.text((125, y), line, font=face, fill=INK)
        y += advance
    return y


centered('LAST WILL AND TESTAMENT', 145, font(49, 'bold'))
centered('of a Grand Theft Auto fan, est. 2013', 225, font(31, 'italic'))
draw.line((230, 295, 970, 295), fill=INK, width=2)

y = paragraph(
    'I, the undersigned, being of sound mind and of truly unreasonable patience, do hereby bequeath:',
    350, font(35),
)
y += 50
clauses = [
    '1. My GTA 6 pre-order — to my grandson. He will know what to do.',
    "2. My 'one more year' meme folder — to the group chat. Suffer as I suffered.",
    '3. My 4,811 days of waiting — to science. Study them.',
    '4. My place in the release-day queue — NON-TRANSFERABLE. Some things are sacred.',
]
for clause in clauses:
    y = paragraph(clause, y, font(35)) + 35

y += 12
y = paragraph('Signed the night before launch, after 13 years of waiting.', y, font(29, 'italic'))
if y > 1240:
    raise ValueError('Body text overlaps the seal')
draw.line((128, y + 38, 610, y + 38), fill=INK, width=2)

# Rotate the whole seal so its lettering and circular outline share the tilt.
seal = Image.new('RGBA', (430, 310), (0, 0, 0, 0))
stamp = ImageDraw.Draw(seal)
red = '#a72e30'
stamp.ellipse((72, 12, 358, 298), outline=red, width=6)
stamp.ellipse((82, 22, 348, 288), outline=red, width=2)
stamp.text((215, 95), 'CERTIFIED BY', font=font(23, 'bold'), fill=red, anchor='mt')
stamp.text((215, 133), 'make.fun', font=font(43, 'bold'), fill=red, anchor='mt')
stamp.text((215, 193), 'skill-based bounties', font=font(19, 'italic'), fill=red, anchor='mt')
seal = seal.rotate(15, resample=Image.Resampling.BICUBIC, expand=True)
page.paste(seal, (665, 1190), seal)

output = Path(__file__).resolve().with_name('meme.png')
page.save(output, format='PNG')
print(f'{output} ({output.stat().st_size} bytes)')
