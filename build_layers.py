"""Split the flat-colour emblem PNGs into per-region coverage masks.

Each output mask is an 8-bit greyscale PNG whose value is the fraction of
that pixel covered by the region (so anti-aliased edges stay smooth).
The web page recolours by summing colour*coverage over all layers.
"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

PALETTE = {               # source colours
    'navy':  (0x22, 0x2A, 0x39),
    'gold':  (0xE0, 0xC7, 0xA9),
    'pink':  (0xDE, 0x80, 0xA6),
    'cream': (0xF4, 0xEE, 0xE8),
    'white': (0xFF, 0xFF, 0xFF),
}
NAMES = list(PALETTE)
P = np.array([PALETTE[n] for n in NAMES], dtype=np.float32)

CROWN_BOX = (1000, 620, 1450, 940)   # x0,y0,x1,y1 region holding the 4 gems
RIBBON_Y  = 1700                      # pink below this line is the ribbon


def unmix(img):
    """Per pixel: weights over palette, using the best 2-colour mix."""
    h, w, _ = img.shape
    px = img.reshape(-1, 3).astype(np.float32)
    best_res = np.full(len(px), np.inf, np.float32)
    best_i = np.zeros(len(px), np.int32); best_j = np.zeros(len(px), np.int32)
    best_t = np.zeros(len(px), np.float32)
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            a, b = P[i], P[j]
            ab = b - a
            t = np.clip(((px - a) @ ab) / (ab @ ab), 0, 1)
            res = np.linalg.norm(px - (a + t[:, None] * ab), axis=1)
            m = res < best_res
            best_res[m] = res[m]; best_i[m] = i; best_j[m] = j; best_t[m] = t[m]
    W = np.zeros((len(px), len(P)), np.float32)
    idx = np.arange(len(px))
    W[idx, best_i] += 1 - best_t
    W[idx, best_j] += best_t
    return W.reshape(h, w, len(P)), best_res.reshape(h, w)


def split_components(weight, hard=0.5):
    """Label connected blobs of a weight map; soft edge pixels inherit the
    label of the nearest blob."""
    lab, n = ndi.label(weight > hard)
    # grow labels outward a few px to cover anti-aliased rims
    grown = lab.copy()
    for _ in range(6):
        d = ndi.grey_dilation(grown, size=3)
        grown = np.where((grown == 0) & (weight > 0), d, grown)
    return grown, n


def build(src, tag, outdir, lineref=None):
    img = np.array(Image.open(src).convert('RGB'))
    H, Wd, _ = img.shape
    W, res = unmix(img)
    print(f'{tag}: max unmix residual {res.max():.1f}, mean {res.mean():.2f}')
    w = {n: W[..., k] for k, n in enumerate(NAMES)}

    layers = {}
    # --- navy: background field vs. thin dark lines inside the art
    if lineref == 'none':
        # source rendered without any navy outlines: every navy pixel is background
        layers['line'] = np.zeros_like(w['navy'])
        layers['bg']   = w['navy']
    elif lineref:
        # reference render of only the navy-outlined shapes (fills off) on white: dark = outline
        ref = np.array(Image.open(lineref).convert('L')) < 160
        ref = ndi.binary_dilation(ref, structure=np.ones((3, 3)), iterations=1)
        layers['line'] = np.where(ref, w['navy'], 0)
        layers['bg']   = np.where(ref, 0, w['navy'])
    else:
        navy_hard = w['navy'] > 0.5
        field = ndi.binary_opening(navy_hard, structure=np.ones((3, 3)), iterations=13)
        field = ndi.binary_dilation(field, structure=np.ones((3, 3)), iterations=1)
        layers['bg']   = np.where(field, w['navy'], 0)
        layers['line'] = np.where(field, 0, w['navy'])

    layers['gold']  = w['gold']
    layers['cream'] = w['cream']
    layers['text']  = w['white']

    # --- pink: wings / ribbon / 4 crown gems
    lab, n = split_components(w['pink'])
    wings = np.zeros_like(w['pink']); ribbon = np.zeros_like(w['pink'])
    gems = []
    x0, y0, x1, y1 = CROWN_BOX
    for k in range(1, n + 1):
        m = lab == k
        ys, xs = np.nonzero(m)
        cy, cx = ys.mean(), xs.mean()
        part = np.where(m, w['pink'], 0)
        if cy > RIBBON_Y:
            ribbon += part
        elif x0 <= cx <= x1 and y0 <= cy <= y1 and m.sum() < 20000:
            gems.append((cx, cy, part))
        else:
            wings += part
    assert len(gems) == 4, f'{tag}: expected 4 gems, found {len(gems)}'
    gems.sort(key=lambda g: g[1])            # topmost first
    top = gems[0]
    band = sorted(gems[1:], key=lambda g: g[0])   # left, mid, right by x
    layers['gem_top']   = top[2]
    layers['gem_left']  = band[0][2]
    layers['gem_mid']   = band[1][2]
    layers['gem_right'] = band[2][2]
    layers['wings']  = wings
    layers['ribbon'] = ribbon

    total = sum(layers.values())
    print(f'{tag}: coverage sum min {total.min():.3f} max {total.max():.3f}')

    names = []
    for name, arr in layers.items():
        if arr.sum() < 100:
            print(f'{tag}: {name} empty, skipped'); continue
        a = np.clip(arr * 255 + 0.5, 0, 255).astype(np.uint8)
        la = np.dstack([np.full_like(a, 255), a])          # white + alpha
        Image.fromarray(la, 'LA').save(f'{outdir}/{tag}_{name}.png', optimize=True)
        names.append(name)
    return {'w': Wd, 'h': H, 'layers': names}


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    suffix = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--suffix=')), '')
    outdir = args[0]
    meta = {}
    refs = {'plain': None, 'ribbon': None, 'text': None}
    if len(args) > 5:            # optional: lineref_plain lineref_ribbon (ribbon ref also serves the text version); 'none' = no outlines in source
        refs = {'plain': args[4], 'ribbon': args[5], 'text': args[5]}
    for tag, src in [('plain', args[1]), ('ribbon', args[2]), ('text', args[3])]:
        meta[tag + suffix] = build(src, tag + suffix, outdir, refs[tag])
    mp = f'{outdir}/meta{suffix}.json'
    json.dump(meta, open(mp, 'w'), indent=1)
    print(json.dumps(meta))
