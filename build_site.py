"""Build index.html (GitHub Pages, uses masks/ folder) and
emblem-colorizer-standalone.html (single file, masks embedded as data URIs)."""
import base64, json, glob, os
page = open('page.html', encoding='utf-8').read()
head = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')
tail = '</body></html>'
open('index.html', 'w', encoding='utf-8').write(head + page + tail)
masks = {}
for f in sorted(glob.glob('masks/*.png')):
    masks[os.path.basename(f)[:-4]] = 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
embed = '<script>window.EMBEDDED_MASKS=' + json.dumps(masks) + '</script>'
open('emblem-colorizer-standalone.html', 'w', encoding='utf-8').write(head + embed + page + tail)
print('index.html', os.path.getsize('index.html'), 'standalone', os.path.getsize('emblem-colorizer-standalone.html'))
