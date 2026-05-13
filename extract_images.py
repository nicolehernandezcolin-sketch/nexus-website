import re, base64, os

src = '/Users/Nicole/nexus-website/index.html'
img_dir = '/Users/Nicole/nexus-website/images'
os.makedirs(img_dir, exist_ok=True)

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

img_tag_re = re.compile(
    r'(<img\b[^>]*?src=")data:image/(png|jpeg|gif|webp);base64,([A-Za-z0-9+/=]+)("[^>]*?>)',
    re.DOTALL
)
used = {}

def slug(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def replacement(m):
    prefix, fmt, b64, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
    full_tag = m.group(0)
    ext = 'jpg' if fmt == 'jpeg' else fmt

    alt_m = re.search(r'alt="([^"]*)"', full_tag)
    cls_m = re.search(r'class="([^"]*)"', full_tag)
    alt = alt_m.group(1) if alt_m else ''
    cls = cls_m.group(1) if cls_m else ''

    if 'dc-photo' in cls:
        section = 'dancer'
    elif 'ac-photo' in cls:
        section = 'artist'
    else:
        section = 'img'

    base = slug(alt) if alt else section
    key = base
    if key in used and used[key] != section:
        base = f'{section}-{base}'
    used[key] = section

    fname = f'{base}.{ext}'
    path = os.path.join(img_dir, fname)

    data = base64.b64decode(b64 + '==')
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  Wrote images/{fname}  ({len(data) // 1024}KB)')

    return f'{prefix}images/{fname}{suffix}'

new_html, count = img_tag_re.subn(replacement, html)
print(f'\n{count} images extracted.')

with open(src, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('HTML updated.')
