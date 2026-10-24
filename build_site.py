"""Build index.html (GitHub Pages, uses masks/ folder), emblem-colorizer-standalone.html (single file,
masks embedded) and artifact.html (page body with the ErinLang font embedded, for the claude.ai artifact)."""
import base64, json, glob, os
page = open('page.html', encoding='utf-8').read()
font_b64 = base64.b64encode(open('ErinLang-Direct.ttf', 'rb').read()).decode()
font_css = "@font-face{font-family:'ErinLang';src:url(data:font/ttf;base64," + font_b64 + ") format('truetype');font-display:block}"
page = page.replace('/*__ERINLANG_FONT__*/', font_css)
head = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')
tail = '</body></html>'
open('artifact.html', 'w', encoding='utf-8').write(page)
open('index.html', 'w', encoding='utf-8').write(head + page + tail)
masks = {}
for f in sorted(glob.glob('masks/ribbon_*.png')):
    masks[os.path.basename(f)[:-4]] = 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
embed = '<script>window.EMBEDDED_MASKS=' + json.dumps(masks) + '</script>'
open('emblem-colorizer-standalone.html', 'w', encoding='utf-8').write(head + embed + page + tail)
print('artifact.html', os.path.getsize('artifact.html'), 'index.html', os.path.getsize('index.html'), 'standalone', os.path.getsize('emblem-colorizer-standalone.html'))
