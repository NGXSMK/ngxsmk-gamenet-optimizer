from PIL import Image, ImageDraw
import os

SIZES = [16, 32, 48, 64, 128, 256]
PRIMARY = (99, 102, 241)
DARK = (79, 70, 229)
LIGHT = (129, 140, 248)
WHITE = (255, 255, 255)

def make_icon(size):
    s = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = s // 2, s // 2
    sh = s * 0.42
    pts = [
        (cx, cy - sh),
        (cx + sh, int(cy - sh * 0.5)),
        (cx + sh, int(cy + sh * 0.2)),
        (cx, int(cy + sh * 0.7)),
        (cx - sh, int(cy + sh * 0.2)),
        (cx - sh, int(cy - sh * 0.5)),
    ]
    draw.polygon(pts, fill=PRIMARY)
    inner = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(inner)
    idraw.polygon(pts, fill=LIGHT)
    mask = Image.new('L', (s, s), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - s * 0.16, cy - s * 0.14, cx + s * 0.16, cy + s * 0.26], fill=180)
    img = Image.composite(inner, img, mask)
    draw = ImageDraw.Draw(img)
    r = s * 0.09
    bd = s * 0.06
    draw.rectangle([cx - r, cy - r * 0.4, cx + r, cy + r * 0.4], fill=WHITE)
    draw.rectangle([cx - r * 0.4, cy - r, cx + r * 0.4, cy + r], fill=WHITE)
    for dx, dy in [(-r * 1.5, -r * 1.5), (r * 1.5, -r * 1.5), (-r * 1.5, r * 1.5), (r * 1.5, r * 1.5)]:
        draw.ellipse([cx + dx - bd, cy + dy - bd, cx + dx + bd, cy + dy + bd], fill=WHITE)
    return img

imgs = [make_icon(s) for s in SIZES]
imgs_dir = os.path.join(os.path.dirname(__file__), '..')
ico_path = os.path.join(imgs_dir, 'icon.ico')

imgs[0].save(ico_path, format='ICO', sizes=[(s, s) for s in SIZES], append_images=imgs[1:])

imgs[-1].save(os.path.join(imgs_dir, 'website', 'public', 'favicon.png'))
print(f"ICO: {ico_path}")
print(f"PNG: website/public/favicon.png")
