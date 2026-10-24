# images/<dir>/<name>.(jpg|png|webp) から images/<dir>/t/<name>.webp（一覧用の軽い画像）と images/full.json を作る
# 使い方: python3 tools/make-thumbs.py   （画像を追加・差し替えたあとに実行）
import os, json
from PIL import Image
R = os.path.join(os.path.dirname(__file__), '..', 'images'); full = {}
for root, ds, fs in os.walk(R):
    if os.path.basename(root) == 't' or os.path.relpath(root, R).split(os.sep)[0] == 'top': continue
    for f in sorted(fs):
        n, e = os.path.splitext(f); e = e.lower().lstrip('.')
        if e not in ('jpg', 'png', 'webp'): continue
        d = os.path.relpath(root, R).replace(os.sep, '/'); full[f'{d}/{n}'] = e
        out = os.path.join(root, 't', n + '.webp')
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(os.path.join(root, f)): continue
        im = Image.open(os.path.join(root, f)); im = im.convert('RGBA' if 'A' in im.getbands() or im.mode == 'P' else 'RGB')
        im.thumbnail((640, 1000), Image.LANCZOS); os.makedirs(os.path.dirname(out), exist_ok=True)
        im.save(out, 'WEBP', quality=78, method=5)
json.dump(full, open(os.path.join(R, 'full.json'), 'w'), ensure_ascii=False, indent=0)
print(len(full), 'files')
