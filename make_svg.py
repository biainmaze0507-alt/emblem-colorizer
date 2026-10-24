"""PDF (slide 1, background rectangle hidden) -> SVG in which every navy area is empty space.

Navy is not a colour of the emblem: background, shield field and all outlines are 'nothing'.
Visible content keeps only the coloured fills; a luminance mask repaints the scene in z-order
(navy -> black, everything else -> white) so the footprint of each navy shape is cut out of
whatever lies beneath it, exactly like the site's transparent export.
Usage: python -I make_svg.py slide1_lines.pdf emblem.svg <folder containing pymupdf>"""
import sys, re
sys.path.insert(0, sys.argv[3])
import warnings; warnings.filterwarnings('ignore')
import fitz

NAVY = '#222a39'
page = fitz.open(sys.argv[1])[0]
svg = page.get_svg_image(matrix=fitz.Matrix(1, 1), text_as_path=True)
svg, n_bg = re.subn(r'<path[^>]*d="M0 [^"]*H540V540[^"]*H0Z"[^>]*fill="#222a39"[^>]*/>\s*', '', svg, flags=re.I)
head, rest = svg.split('</defs>', 1)
body = rest.rsplit('</svg>', 1)[0]

# --- mask: same geometry, navy -> black, any other colour -> white
other = re.compile(r'(fill|stroke)="#(?!222a39)[0-9a-f]{6}"', re.I)
navy = re.compile(r'(fill|stroke)="#222a39"', re.I)
mask_body = navy.sub(lambda m: m.group(1) + '="#000000"', other.sub(lambda m: m.group(1) + '="#ffffff"', body))
mask = ('<mask id="navycut" maskUnits="userSpaceOnUse" x="0" y="0" width="540" height="540">'
        '<rect x="0" y="0" width="540" height="540" fill="#ffffff"/>' + mask_body + '</mask>')

# --- visible content: remove navy elements; keep coloured fills that merely had a navy stroke
def clean_path(m):
    tag = m.group(0)
    fill = re.search(r'fill="([^"]*)"', tag, re.I)
    stroke = re.search(r'stroke="([^"]*)"', tag, re.I)
    fill_v = fill.group(1).lower() if fill else 'none'
    stroke_v = stroke.group(1).lower() if stroke else 'none'
    navy_fill = fill_v == NAVY
    navy_stroke = stroke_v == NAVY
    if navy_fill and (stroke_v in ('none', NAVY)):
        return ''                                   # pure navy shape: gone
    if navy_stroke:
        tag = re.sub(r'\s(stroke|stroke-width|stroke-linecap|stroke-linejoin|stroke-miterlimit|stroke-dasharray)="[^"]*"', '', tag, flags=re.I)
        if navy_fill: tag = re.sub(r'\sfill="#222a39"', ' fill="none"', tag, flags=re.I)
    return tag
vis = re.sub(r'<path\b[^>]*/>', clean_path, body, flags=re.I)

out = head + mask + '</defs>\n<g mask="url(#navycut)">' + vis + '</g>\n</svg>\n'
from xml.etree import ElementTree as ET; ET.fromstring(out)
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print('bg rects removed', n_bg, '| mask colours', sorted(set(re.findall(r'(?:fill|stroke)="(#[0-9a-f]{6})"', mask_body, re.I))),
      '| navy refs left in visible content', len(navy.findall(vis)), '| bytes', len(out))
