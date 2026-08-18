#!/usr/bin/env python3
"""Build 'Grandma on the Farm' — cookbook HTML (print + web) from merged.json."""
import json, re, html, os, sys, base64, subprocess, collections
from illos import ILLOS

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.dirname(HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCRATCH, 'out')
os.makedirs(OUT, exist_ok=True)

m = json.load(open(os.path.join(HERE, 'merged.json')))
recipes = m['recipes']; extras = m['extras']
R = {r['id']: r for r in recipes}

# ---------------------------------------------------------------- fixes
# Lasagna: photo 458 ("Lasagna - cont'd", filed under Meats) is the second card of 546.
if 458 in R and 546 in R:
    a, b = R[546], R[458]
    a['photos'] += b['photos']; a['ingredients'] += b['ingredients']; a['directions'] += b['directions']
    a['notes'] = [n for n in a['notes'] if 'no assembly' not in n] + ['Second card is headed "Lasagna – cont\'d".']
    recipes.remove(b); del R[458]
R[76]['title'] = 'Peach Iced Tea'
R[587]['title'] = 'Ham & Corn Chowder'
R[587]['notes'].insert(0, 'The clipping\'s title is cut off; the name here is ours.')

# ---------------------------------------------------------------- chapters
CHAPTERS = [
    ('bev',   'Beverages & Punches',              'teapot'),
    ('hors',  "Hors d'Oeuvres, Dips & Sandwiches",'platter'),
    ('bread', 'Breads, Buns & Muffins',           'bread'),
    ('bkfst', 'Breakfast, Eggs & Cheese',         'eggs'),
    ('soup',  'Soups & Stews',                    'pot'),
    ('salad', 'Salads & Dressings',               'salad'),
    ('meat',  'Meats',                            'skillet'),
    ('poul',  'Poultry & Stuffings',              'rooster'),
    ('fish',  'Fish & Seafoods',                  'fish'),
    ('cass',  'Casseroles',                       'casserole'),
    ('veg',   'Vegetables',                       'veg'),
    ('sauce', 'Sauces',                           'sauce'),
    ('pie',   'Pies & Pastries',                  'pie'),
    ('dess',  'Desserts & Puddings',              'bowl'),
    ('bars',  'Slices, Bars & Sweet Treats',      'cookies'),
    ('frost', 'Frostings & Fillings',             'cake'),
    ('pres',  'Preserves, Pickles & Pantry',      'jars'),
]
CH = {k: t for k, t, _ in CHAPTERS}
SECTION_TO_CH = {
    'Breads': 'bread', 'Pies & Pastries': 'pie', 'Casseroles': 'cass', 'Desserts & Puddings': 'dess',
    'Slices & Bars': 'bars', 'Eggs & Cheese': 'bkfst', 'Fish & Seafoods': 'fish', 'Frostings & Fillings': 'frost',
    "Hors d'Oeuvres": 'hors', 'Meats': 'meat', 'Poultry & Stuffings': 'poul', 'Preserves & Jellies': 'pres',
    'Salads & Dressings': 'salad', 'Sandwiches': 'hors', 'Sauces': 'sauce', 'Soups & Stews': 'soup', 'Vegetables': 'veg',
}
CAT_TO_CH = {
    'Breads & Buns': 'bread', 'Breakfast': 'bkfst', 'Soups & Salads': 'salad', 'Main Dishes': 'meat',
    'Vegetables & Sides': 'veg', 'Cookies & Bars': 'bars', 'Cakes & Frostings': 'dess', 'Pies & Pastry': 'pie',
    'Desserts & Sweets': 'dess', 'Candy & Treats': 'bars', 'Preserves, Pickles & Sauces': 'pres', 'Beverages': 'bev',
    'Other': 'hors',
}
OVERRIDE = {  # id -> chapter, for cards outside her tabbed sections or clearly misfiled
    1:'bread', 3:'salad', 4:'bev', 6:'fish', 13:'bars', 14:'bkfst', 16:'meat', 18:'cass', 21:'bars', 23:'salad', 24:'salad',
    25:'hors', 26:'hors', 29:'bkfst', 30:'dess', 32:'bkfst', 33:'bread', 35:'bev', 38:'meat', 48:'hors', 49:'hors', 50:'hors',
    51:'salad', 52:'pres', 54:'hors', 61:'dess', 82:'hors', 122:'bev', 404:'hors', 546:'cass',
    607:'bars', 608:'salad', 609:'bkfst', 610:'salad', 611:'cass', 612:'soup', 614:'bev', 615:'meat', 617:'bkfst', 619:'hors',
    620:'veg', 621:'bev', 622:'pres', 624:'bars', 625:'bev', 626:'dess', 628:'pres', 629:'salad', 630:'pres', 631:'dess', 633:'meat',
}
for r in recipes:
    if r['id'] in OVERRIDE: r['ch'] = OVERRIDE[r['id']]; r['placed'] = 'ours'
    elif r['section'] in SECTION_TO_CH: r['ch'] = SECTION_TO_CH[r['section']]; r['placed'] = 'hers'
    else: r['ch'] = CAT_TO_CH.get(r['agent_category'], 'hors'); r['placed'] = 'ours'
# order: her tabbed cards first (photo order), then the loose/misc ones
by_ch = collections.OrderedDict((k, []) for k, _, _ in CHAPTERS)
for r in sorted(recipes, key=lambda r: (r['placed'] != 'hers', r['id'])):
    by_ch[r['ch']].append(r)

# ---------------------------------------------------------------- text helpers
FRAC = {'1/2':'½','1/4':'¼','3/4':'¾','1/3':'⅓','2/3':'⅔','1/8':'⅛','3/8':'⅜','5/8':'⅝','7/8':'⅞'}
def nice(s):
    if s is None: return ''
    s = html.escape(s, quote=False)
    s = re.sub(r'(?<![\d/])(\d+)/(\d+)(?![\d/])', lambda mm: FRAC.get(mm.group(0), mm.group(0)), s)
    s = re.sub(r'(?<=\d) (?=[½¼¾⅓⅔⅛⅜⅝⅞])', ' ', s)          # 1 ½ -> 1 ½ (thin space)
    s = re.sub(r'(?<=\d)(?=[½¼¾⅓⅔⅛⅜⅝⅞])', ' ', s)
    s = s.replace(' - ', ' – ').replace('--', '—')
    s = re.sub(r'"([^"]*)"', '“\\1”', s)
    s = s.replace("'", '’')
    s = re.sub(r'\[\?\]', '<span class="unsure">[?]</span>', s)
    s = re.sub(r'\[([^\]]+)\?\]', '<span class="unsure">[\\1?]</span>', s)
    return s

def slug(s): return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')

MARK = re.compile(r'^===\s*(.*?)\s*===\s*(.*)$')
PREFIX = re.compile(r'^(first|second|third|fourth|fifth|sixth)\s*(card|recipe)?\s*:\s*', re.I)
def segments(r):
    """Split ingredients/directions into sub-recipes at === markers. Returns list of dict(title, ings, dirs)."""
    segs = []
    def seg_for(title):
        for s in segs:
            if s['title'] == title: return s
        s = {'title': title, 'ings': [], 'dirs': []}; segs.append(s); return s
    for field, key in (('ingredients', 'ings'), ('directions', 'dirs')):
        cur = seg_for(None)
        for line in r[field]:
            mm = MARK.match(line)
            if mm:
                t = PREFIX.sub('', mm.group(1)).strip()
                cur = seg_for(t)
                if mm.group(2).strip(): cur[key].append(mm.group(2).strip())
                continue
            cur[key].append(line)
    segs = [s for s in segs if s['ings'] or s['dirs']]
    if segs and segs[0]['title'] is None and len(segs) > 1 and r['title'] and ' / ' in r['title']:
        segs[0]['title'] = r['title'].split(' / ')[0]
    return segs

def ing_html(lines):
    out = []
    for l in lines:
        mm = re.match(r'^[—–-]\s*(.*?)\s*[—–-]$', l.strip())
        if mm and len(l) < 60: out.append(f'<li class="sub">{nice(mm.group(1))}</li>')
        else: out.append(f'<li>{nice(l)}</li>')
    return f'<ul class="ing{" long" if len(lines) > 11 else ""}">' + ''.join(out) + '</ul>'

def dir_html(lines):
    return ''.join(f'<p>{nice(l)}</p>' for l in lines)

def caption_for(r):
    n = len(r['photos'])
    if r['kind'] == 'clipping':
        return 'The clipping she kept' if n == 1 else 'The clipping she kept, front and back'
    return {1: 'Grandma’s card', 2: 'Grandma’s card, front and back'}.get(n, 'Grandma’s cards')

# ---------------------------------------------------------------- image handling
IMG_MODE = os.environ.get('IMG_MODE', 'file')   # file | inline | none
def img_src(n):
    if IMG_MODE == 'inline':
        p = os.path.join(HERE, 'cards_web', f'{n:03d}.jpg')
        return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return f'cards/{n:03d}.jpg'

def facsimile(r):
    if IMG_MODE == 'none': return ''
    imgs = ''.join(f'<img src="{img_src(n)}" alt="Photograph of the original handwritten card">' for n in r['photos'])
    return f'<figure class="fac n{min(len(r["photos"]),3)}">{imgs}<figcaption>{caption_for(r)}</figcaption></figure>'

# ---------------------------------------------------------------- recipe rendering
def recipe_html(r, kindlabel=True):
    rid = f"r{r['id']}"
    segs = segments(r)
    parts = []
    parts.append(f'<article class="recipe" id="{rid}">')
    parts.append(f'<span class="pm">⟦{rid}⟧</span>')
    head = f'<h3 class="rtitle">{nice(r["title"])}</h3>'
    meta = []
    if r['attribution']: meta.append(f'<span class="from">{nice(r["attribution"])}</span>')
    if r['kind'] == 'clipping' and kindlabel: meta.append('<span class="tag">clipping</span>')
    parts.append(f'<header>{head}' + (('<div class="meta">' + ' '.join(meta) + '</div>') if meta else '') + '</header>')
    fac = facsimile(r)
    parts.append('<div class="rgrid' + (' nofac' if not fac else '') + '"><div class="rtext">')
    for s in segs:
        if s['title']: parts.append(f'<h4 class="subrecipe">{nice(s["title"])}</h4>')
        cols = []
        if s['ings']: cols.append('<div class="ings">' + ing_html(s['ings']) + '</div>')
        if s['dirs']: cols.append('<div class="dirs">' + dir_html(s['dirs']) + '</div>')
        parts.append(f'<div class="body {"one" if len(cols)==1 else ""}">' + ''.join(cols) + '</div>')
    META = re.compile(r'continues|back of|front of|\bcard\b|cards\b|photo|duplicate|shot|cropped|cut off|edge|\bink\b|pencil|handwrit|typewrit|typed|printed|clipping|notepaper|\bslip\b|framing|transcri|legible|readable|this side|second card|first card|attribution|title|written|crossed|smudg|stain|worn|faded|marker|margin', re.I)
    notes = [n for n in r['notes'] if not META.search(n) and (not r['attribution'] or r['attribution'].lower() not in n.lower())]
    if r['confidence'] == 'medium':
        notes.append('A few words on this card were hard to make out — check the original.')
    if notes:
        parts.append('<div class="notes">' + ''.join(f'<p>{nice(n)}</p>' for n in notes) + '</div>')
    parts.append('</div>' + fac + '</div>')
    parts.append('</article>')
    return ''.join(parts)

# ---------------------------------------------------------------- page numbers (from a previous pass)
PAGES = {}
pf = os.path.join(OUT, 'pages.json')
if os.path.exists(pf): PAGES = json.load(open(pf))
def pg(key): return PAGES.get(key, '')
BLANKS = set()
bf = os.path.join(OUT, 'blanks.json')
if os.path.exists(bf): BLANKS = set(json.load(open(bf)))
def blank_before(key):
    return '<div class="blankpage"></div>' if key in BLANKS else ''

# ---------------------------------------------------------------- CSS
INK = '#2E4A8B'; CREAM = '#FBF8F0'; TAB = '#E8C547'; GREEN = '#4B6B58'; PENCIL = '#6B6B66'; RULE = '#C9D6EA'
chapter_pages_css = ''.join(
    f'@page {k} {{ @top-right {{ content: "{t}"; }} }} @page {k}:left {{ @top-right {{ content: none; }} @top-left {{ content: "Grandma on the Farm"; }} }}\n'
    for k, t, _ in CHAPTERS + [('extra', 'Crafts, Hints & Remedies', ''), ('back', 'Index', '')])

CSS = f'''
:root {{ --ink:{INK}; --cream:{CREAM}; --tab:{TAB}; --green:{GREEN}; --pencil:{PENCIL}; --rule:{RULE}; --paper:#ffffff; --text:#1f2430; }}
@page {{ size: 8.5in 11in; margin: 0.8in 0.8in 0.8in 0.8in;
  @bottom-center {{ content: counter(page); font-family: Baskerville, "Libre Baskerville", Georgia, serif; font-size: 9.5pt; color: {PENCIL}; }}
  @top-left {{ font-family: Baskerville, Georgia, serif; font-size: 8.5pt; font-style: italic; color: {PENCIL}; content: "Grandma on the Farm"; }}
  @top-right {{ font-family: Baskerville, Georgia, serif; font-size: 8.5pt; font-style: italic; color: {PENCIL}; }} }}
@page :left {{ margin-left: 0.8in; margin-right: 1.05in; }}
@page :right {{ margin-left: 1.05in; margin-right: 0.8in; }}
@page :left {{ @top-left {{ content: "Grandma on the Farm"; }} }}
@page :right {{ @top-left {{ content: none; }} }}
@page bleed {{ margin: 0; @bottom-center {{ content: none; }} @top-left {{ content: none; }} @top-right {{ content: none; }} }}
@page blank {{ @bottom-center {{ content: none; }} @top-left {{ content: none; }} @top-right {{ content: none; }} }}
.blankpage {{ page: blank; break-before: page; break-after: page; min-height: 1px; }}
@page front {{ @bottom-center {{ content: none; }} @top-left {{ content: none; }} @top-right {{ content: none; }} }}
{chapter_pages_css}
* {{ box-sizing: border-box; }}
a {{ color: inherit; text-decoration: none; }}
html, body {{ margin: 0; padding: 0; background: var(--paper); color: var(--text); }}
body {{ font-family: Baskerville, "Libre Baskerville", Georgia, "Times New Roman", serif; font-size: 10.3pt; line-height: 1.4; }}
.pm {{ font-size: 1px; color: #fff; position: absolute; }}
.script {{ font-family: "Snell Roundhand", "Apple Chancery", "Brush Script MT", cursive; font-weight: 400; }}
.sc {{ font-variant: small-caps; letter-spacing: 0.08em; }}
.unsure {{ color: var(--pencil); }}
.illo {{ display: block; width: 100%; height: auto; }}
/* ---- cover */
.cover {{ page: bleed; break-after: page; width: 8.5in; height: 11in; background: var(--green); color: var(--cream); position: relative; overflow: hidden; }}
.cover .frame {{ position: absolute; inset: 0.55in; border: 1.5px solid rgba(251,248,240,.55); }}
.cover .frame2 {{ position: absolute; inset: 0.65in; border: 0.5px solid rgba(251,248,240,.4); }}
.cover .art {{ position: absolute; top: 1.35in; left: 1.6in; right: 1.6in; }}
.cover .title {{ position: absolute; top: 5.05in; left: 0; right: 0; text-align: center; font-size: 60pt; line-height: 1.05; }}
.cover .sub {{ position: absolute; top: 7.15in; left: 1in; right: 1in; text-align: center; font-size: 12.5pt; letter-spacing: 0.22em; text-transform: uppercase; }}
.cover .sub2 {{ position: absolute; top: 7.65in; left: 1in; right: 1in; text-align: center; font-size: 11pt; font-style: italic; opacity: .9; }}
.cover .foot {{ position: absolute; bottom: 0.95in; left: 1in; right: 1in; text-align: center; font-size: 9pt; letter-spacing: 0.18em; text-transform: uppercase; opacity: .85; }}
.cover .wheat {{ position: absolute; bottom: 1.35in; left: 3.6in; right: 3.6in; opacity: .9; }}
/* ---- front matter */
.fm {{ page: front; break-after: page; min-height: 8in; position: relative; }}
.halftitle {{ text-align: center; padding-top: 3.2in; font-size: 30pt; color: var(--ink); }}
.titlepage {{ text-align: center; padding-top: 1.2in; color: var(--ink); }}
.titlepage .art {{ width: 3.4in; margin: 0 auto 0.3in; }}
.titlepage .t {{ font-size: 46pt; line-height: 1.1; }}
.titlepage .s {{ font-size: 11.5pt; letter-spacing: .2em; text-transform: uppercase; margin-top: .55in; }}
.titlepage .s2 {{ font-style: italic; margin-top: .25in; color: var(--pencil); font-size: 11pt; }}
.titlepage .pub {{ position: absolute; bottom: 0.4in; left: 0; right: 0; font-size: 9.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--pencil); }}
.colophon {{ font-size: 9.2pt; color: var(--pencil); padding-top: 6.5in; line-height: 1.5; }}
.colophon p {{ margin: 0 0 .5em; }}
.dedication {{ text-align: center; padding-top: 3.4in; font-style: italic; font-size: 13pt; color: var(--ink); line-height: 1.6; }}
.dedication .art {{ width: 1.5in; margin: 0 auto .5in; opacity: .9; }}
.prose {{ max-width: 5.6in; }}
.prose h2 {{ font-weight: 400; color: var(--ink); font-size: 24pt; margin: 0 0 .5em; }}
.prose h2 .script {{ font-size: 30pt; }}
.prose p {{ margin: 0 0 .7em; text-align: justify; hyphens: auto; }}
.prose p.first::first-letter {{ font-size: 3.1em; float: left; line-height: .85; padding: .06em .08em 0 0; color: var(--ink); }}
.key {{ margin: .6em 0 0; padding: 0; list-style: none; columns: 2; column-gap: .4in; font-size: 9.8pt; }}
.key li {{ break-inside: avoid; margin: 0 0 .35em; padding-left: 1.3in; text-indent: -1.3in; }}
.key b {{ font-weight: 600; color: var(--ink); display: inline-block; width: 1.25in; text-indent: 0; }}
/* ---- contents */
.toc h2 {{ font-weight: 400; color: var(--ink); font-size: 34pt; margin: .2in 0 .35in; }}
.toc ol {{ list-style: none; margin: 0; padding: 0; }}
.toc li {{ display: flex; align-items: baseline; gap: .12in; margin: 0 0 .13in; font-size: 12.5pt; }}
.toc li .n {{ color: var(--pencil); font-size: 9pt; width: .28in; letter-spacing: .05em; }}
.toc li .t {{ }}
.toc li .dots {{ flex: 1; border-bottom: 1px dotted var(--rule); transform: translateY(-.25em); }}
.toc li .p {{ font-variant-numeric: tabular-nums; color: var(--ink); }}
.toc li.small {{ font-size: 10.5pt; margin-top: .25in; }}
/* ---- chapter opener */
.chapter {{ break-before: right; break-after: page; text-align: left; position: relative; }}
.chapter .tab {{ display: inline-block; background: var(--tab); color: #3d3410; font-size: 8.5pt; letter-spacing: .2em; text-transform: uppercase; padding: 3px 12px 2px; border-radius: 3px 3px 0 0; }}
.chapter .rulebar {{ height: 1.5px; background: var(--ink); margin: 0 0 .35in; }}
.chapter .art {{ width: 2.6in; margin: .1in 0 .05in; color: var(--ink); }}
.chapter h2 {{ font-weight: 400; color: var(--ink); font-size: 34pt; line-height: 1.1; margin: 0 0 .1in; text-wrap: balance; }}
.chapter .count {{ color: var(--pencil); font-style: italic; margin: 0 0 .3in; }}
.chapter ul.list {{ list-style: none; margin: 0; padding: 0; columns: 2; column-gap: .45in; font-size: 9.6pt; line-height: 1.35; }}
.chapter ul.list li {{ display: flex; align-items: baseline; gap: .06in; break-inside: avoid; margin-bottom: .04in; }}
.chapter ul.list .t {{ }}
.chapter ul.list .dots {{ flex: 1; border-bottom: 1px dotted var(--rule); min-width: .2in; transform: translateY(-.25em); }}
.chapter ul.list .p {{ font-variant-numeric: tabular-nums; color: var(--ink); }}
/* ---- recipes */
.recipe {{ break-inside: avoid; margin: 0 0 .22in; padding: 0 0 .1in; border-bottom: 1px solid var(--rule); position: relative; }}
.recipe:last-child {{ border-bottom: 0; }}
.recipe header {{ margin: 0 0 .09in; }}
.rtitle {{ font-weight: 400; font-size: 16.5pt; line-height: 1.15; color: var(--ink); margin: 0; letter-spacing: .005em; text-wrap: balance; }}
.meta {{ margin-top: .03in; font-size: 9.6pt; color: var(--pencil); }}
.meta .from {{ font-style: italic; }}
.meta .from::before {{ content: "from "; }}
.meta .tag {{ font-style: normal; font-size: 7.5pt; letter-spacing: .16em; text-transform: uppercase; border: 1px solid var(--rule); padding: 1px 6px 0; margin-left: .1in; border-radius: 2px; vertical-align: 1px; }}
.rgrid {{ display: grid; grid-template-columns: minmax(0, 1fr) 3.35in; gap: 0 .3in; align-items: start; }}
.rgrid.nofac {{ grid-template-columns: 1fr; }}
.subrecipe {{ font-weight: 400; font-size: 11.5pt; color: var(--ink); margin: .1in 0 .04in; font-variant: small-caps; letter-spacing: .06em; }}
.subrecipe:first-child {{ margin-top: 0; }}
.body {{ display: block; }}
.ing {{ list-style: none; margin: 0 0 .09in; padding: 0; font-size: 9.7pt; line-height: 1.36; }}
.ing.long {{ columns: 2; column-gap: .22in; }}
.ing li {{ padding-left: .14in; text-indent: -.14in; margin: 0 0 .015in; break-inside: avoid; }}
.ing li.sub {{ font-variant: small-caps; letter-spacing: .06em; color: var(--ink); margin-top: .07in; text-indent: 0; padding-left: 0; }}
.ing li.sub:first-child {{ margin-top: 0; }}
.dirs p {{ margin: 0 0 .42em; }}
.dirs p:last-child {{ margin-bottom: 0; }}
.notes {{ margin: .08in 0 0; font-size: 9pt; font-style: italic; color: var(--pencil); }}
.notes p {{ margin: 0 0 .12em; }}
.notes p::before {{ content: "✎ "; font-style: normal; }}
figure.fac {{ margin: .05in 0 0; padding: 0; display: block; }}
figure.fac img {{ display: block; max-width: 100%; max-height: 3.1in; width: auto; height: auto; margin: 0 auto .08in; border: 1px solid #d8d4c8; box-shadow: 0 1px 2px rgba(0,0,0,.12); }}
figure.fac.n3 {{ display: grid; grid-template-columns: 1fr 1fr; gap: .06in; }}
figure.fac.n3 img {{ margin: 0; }}
figure.fac figcaption {{ font-size: 7.8pt; color: var(--pencil); font-style: italic; text-align: center; margin-top: -.02in; }}
figure.fac.n3 figcaption {{ grid-column: 1 / -1; }}
/* ---- back matter */
.back {{ page: back; break-before: right; }}
.back h2 {{ font-weight: 400; color: var(--ink); font-size: 30pt; margin: 0 0 .25in; }}
.index {{ columns: 3; column-gap: .3in; font-size: 8.9pt; line-height: 1.32; }}
.index .letter {{ break-after: avoid; font-size: 13pt; color: var(--ink); margin: .12in 0 .04in; }}
.index .letter:first-child {{ margin-top: 0; }}
.index div.e {{ display: flex; gap: .05in; align-items: baseline; break-inside: avoid; }}
.index .e .dots {{ flex: 1; border-bottom: 1px dotted var(--rule); min-width: .12in; transform: translateY(-.25em); }}
.index .e .p {{ font-variant-numeric: tabular-nums; color: var(--ink); }}
.people {{ columns: 2; column-gap: .4in; font-size: 9.2pt; }}
.people div.e {{ break-inside: avoid; margin-bottom: .09in; padding-left: .18in; text-indent: -.18in; }}
.people b {{ font-weight: 600; color: var(--ink); }}
.people .p {{ color: var(--pencil); }}
.endnote {{ page: front; break-before: page; text-align: center; padding-top: 3.5in; color: var(--ink); }}
.endnote .art {{ width: 1.8in; margin: 0 auto .4in; }}
'''

SCREEN_CSS = '''
/* ---- screen only */
@media screen {
  body { background: #e9e6dd; }
  .page { background: #fff; max-width: 8.5in; margin: 0 auto; padding: .9in .8in; box-shadow: 0 2px 14px rgba(0,0,0,.08); }
  .cover { margin: 0 auto; }
  .fm, .chapter, .back { min-height: 0; padding-top: 0; }
  .fm { padding: .8in 0; }
  .halftitle { padding-top: 1in; }
  .titlepage { padding-top: .2in; }
  .titlepage .pub { position: static; margin-top: .6in; }
  .colophon { padding-top: 1in; }
  .dedication { padding-top: 1.2in; }
  .endnote { padding-top: 1in; }
  .chapter { padding-top: .2in; }
  .pm { display: none; }
  .toc a, .chapter a, .index a { color: inherit; text-decoration: none; }
  .toc a:hover, .chapter a:hover, .index a:hover { text-decoration: underline; }
}
  .cover { width: 100%; height: auto; min-height: 0; padding: 9% 7% 7%; display: flex; flex-direction: column; align-items: center; gap: .35in; }
  .cover .frame, .cover .frame2 { inset: 4%; }
  .cover .art, .cover .title, .cover .sub, .cover .sub2, .cover .foot, .cover .wheat { position: static; width: auto; max-width: 100%; }
  .cover .art { width: min(60%, 5in); }
  .cover .title { font-size: clamp(30pt, 8vw, 60pt); }
  .cover .sub { font-size: clamp(8pt, 1.8vw, 12.5pt); margin-top: -.2in; }
  .cover .sub2 { margin-top: -.3in; }
  .cover .wheat { width: 1.2in; margin-top: .2in; }
  .cover .foot { margin-top: -.2in; }
  .tocjump { position: fixed; right: 14px; bottom: 14px; background: #2E4A8B; color: #FBF8F0; font-family: Baskerville, Georgia, serif; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; padding: 8px 12px; border-radius: 3px; text-decoration: none; box-shadow: 0 2px 8px rgba(0,0,0,.2); }
  .tocjump:hover { background: #4B6B58; }
  .webnote { max-width: 8.5in; margin: 0 auto; padding: .4in .8in 0; font-family: Baskerville, Georgia, serif; font-size: 12px; color: #6B6B66; font-style: italic; }
}
@media (max-width: 700px) {
  .page { padding: .5in .35in; }
  .index { columns: 2; }
  .rgrid { grid-template-columns: 1fr; }
  .index { columns: 2; }
  .chapter ul.list, .people, .key { columns: 1; }
  .cover { transform-origin: top left; }
}
'''

# ---------------------------------------------------------------- content pieces
def cover_html():
    return f'''<div class="cover">
  <div class="frame"></div><div class="frame2"></div>
  <div class="art">{ILLOS['farm']}</div>
  <div class="title script">Grandma on the Farm</div>
  <div class="sub">Recipes from the kitchen of Grandma Harris</div>
  <div class="sub2">the whole recipe box, in her own hand</div>
  <div class="wheat">{ILLOS['wheat']}</div>
  <div class="foot">A family cookbook</div>
</div>'''

def front_matter(counts):
    n_recipes = sum(len(v) for v in by_ch.values())
    n_cards = len(set(p for r in recipes for p in r['photos'])) + len(set(p for e in extras for p in e['photos']))
    return f'''
<div class="fm halftitle script">Grandma on the Farm</div>
<div class="fm titlepage">
  <div class="art">{ILLOS['milkcan']}</div>
  <div class="t script">Grandma on the Farm</div>
  <div class="s">Recipes from the kitchen of Grandma Harris</div>
  <div class="s2">Every card, note and clipping from her recipe box —<br>transcribed as she wrote them, with the originals alongside</div>
  <div class="pub">A family cookbook · 2026</div>
</div>
<div class="fm colophon">
  <p>Assembled in 2026 from the {n_cards} photographed cards, slips, and clippings in Grandma Harris’s green recipe box. Everything here is set down the way she wrote it — her abbreviations, her asides, her “V.G.” — and each recipe is followed by a photograph of the original card, so the shorthand can always be checked against her hand.</p>
  <p>Where a card was worn or a word was hard to read, the doubtful reading is marked <span class="unsure">[like this?]</span>. Recipes credited to friends and family are credited as she credited them. Recipes on printed clippings are reproduced for the family only.</p>
  <p>Set in Baskerville, with Snell Roundhand for the title. The line drawings are pen-and-ink in the spirit of a doodle in the margin of a card.</p>
</div>
<div class="fm dedication">
  <div class="art">{ILLOS['wheat']}</div>
  For Grandma on the Farm,<br>and for everyone who ever pulled a chair up to her table.
</div>
<div class="fm prose">
  <h2><span class="script">About</span> this book</h2>
  <p class="first">The green metal box sat in the kitchen for decades and slowly filled up: index cards in blue ballpoint, recipes copied out of the Mennonite cookbook and the Best of Bridge, clippings from the Herald and the Co-op paper, a slip from a lady in the hospital, a punch from the gas company, and a stack of children’s crafts and household hints tucked in the front. Behind the yellow tab dividers — <span class="sc">Breads</span>, <span class="sc">Pies &amp; Pastries</span>, <span class="sc">Casseroles</span>, <span class="sc">Fish &amp; Seafoods</span>, <span class="sc">Preserves &amp; Jellies</span> and the rest — is the record of a lifetime of feeding people.</p>
  <p>This book keeps her order. The chapters follow her own tabs, and inside each chapter the cards run in the order she kept them, so recipes that lived side by side in the box still do. Loose cards from the front of the box and the <span class="sc">Miscellaneous</span> tab have been slipped into the chapter where they belong. Nothing has been “improved,” corrected, or modernized: if she wrote <i>oleo</i>, it says oleo; if she wrote <i>bake till done</i>, that is the instruction, and you will have to know your oven the way she knew hers.</p>
  <p>Below every recipe is a photograph of the original card — front and back when she ran onto the back — so the book is also a facsimile of the box. Her handwriting is part of the recipe.</p>
  <h2 style="margin-top:.35in;font-size:18pt"><span class="script" style="font-size:24pt">Reading</span> her cards</h2>
  <p>A short key to the shorthand she used, some of it borrowed from a nurse’s charting hand:</p>
  <ul class="key">
    <li><b>c̄</b> with (a bar over the c — the old Latin <i>cum</i>)</li>
    <li><b>H2O</b> water</li>
    <li><b>oleo</b> margarine</li>
    <li><b>V.G.</b> very good — her highest rating</li>
    <li><b>c, tsp, tbsp</b> cup, teaspoon, tablespoon</li>
    <li><b>tin</b> a can</li>
    <li><b>icing sugar</b> powdered / confectioners’ sugar</li>
    <li><b>pkg.</b> package</li>
    <li><b>lg., sm., med.</b> large, small, medium</li>
    <li><b>dbl.</b> double (or “doubled”)</li>
    <li><b>Best of Bridge</b> the Calgary cookbook series she copied from often</li>
    <li><b>M.A.</b> Mary Ann — whose recipes came all the way from Australia</li>
    <li><b>“our Margaret,” “our Joe”</b> family, as she named them on the cards</li>
    <li><b>re</b> “from” or “as told to me by”</li>
    <li><b>over</b> the recipe continues on the back of the card</li>
    <li><b>350°</b> Fahrenheit, always</li>
  </ul>
</div>'''

def toc_html():
    items = []
    for i, (k, t, _) in enumerate(CHAPTERS, 1):
        items.append(f'<li><span class="n">{i}</span><a href="#ch-{k}"><span class="t">{t}</span></a><span class="dots"></span><span class="p">{pg("ch-"+k)}</span></li>')
    items.append(f'<li class="small"><span class="n"></span><a href="#ch-extra"><span class="t">From the front of the box: crafts, hints &amp; remedies</span></a><span class="dots"></span><span class="p">{pg("ch-extra")}</span></li>')
    items.append(f'<li class="small" style="margin-top:.05in"><span class="n"></span><a href="#people"><span class="t">The people in her recipes</span></a><span class="dots"></span><span class="p">{pg("people")}</span></li>')
    items.append(f'<li class="small" style="margin-top:.05in"><span class="n"></span><a href="#index"><span class="t">Index of recipes</span></a><span class="dots"></span><span class="p">{pg("index")}</span></li>')
    return f'<div class="fm toc" id="toc"><span class="pm">⟦toc⟧</span><h2><span class="script">Contents</span></h2><ol>{"".join(items)}</ol></div>'

def chapter_html(k, t, illo, items, extra=False):
    lis = ''.join(f'<li><a href="#r{r["id"]}"><span class="t">{nice(r["title"])}</span></a><span class="dots"></span><span class="p">{pg("r"+str(r["id"]))}</span></li>' for r in items)
    n = len(items)
    count = f'{n} recipes' if not extra else f'{n} cards'
    if not extra:
        hers = sum(1 for r in items if r['placed'] == 'hers')
        if hers and hers < n: count += f' — {hers} from behind her tab, {n-hers} slipped in from the front of the box'
    return blank_before('ch-'+k) + f'''<div class="chapter" id="ch-{k}" style="page: {k}"><span class="pm">⟦ch-{k}⟧</span>
  <span class="tab">{t if len(t) < 30 else t.split(",")[0]}</span><div class="rulebar"></div>
  <div class="art">{ILLOS[illo]}</div>
  <h2>{t}</h2>
  <p class="count">{count}</p>
  <ul class="list">{lis}</ul>
</div>
<section class="chap" style="page: {k}">{"".join(recipe_html(r) for r in items)}</section>'''

def people_html():
    ppl = collections.defaultdict(list)
    for r in recipes:
        a = r['attribution']
        if not a: continue
        ppl[a].append(r)
    keys = sorted(ppl, key=lambda s: re.sub(r'^(mrs\.?|mr\.?|our|re|from|the|dr\.?)\s+', '', s.lower()))
    rows = ''.join(f'<div class="e"><b>{nice(a)}</b> — ' + '; '.join(f'{nice(r["title"])} <span class="p">{pg("r"+str(r["id"]))}</span>' for r in ppl[a]) + '</div>' for a in keys)
    return blank_before('people') + f'<div class="back" id="people"><span class="pm">⟦people⟧</span><h2><span class="script">The people</span> in her recipes</h2><p style="max-width:5.6in;margin:0 0 .3in;color:var(--pencil);font-style:italic">Grandma credited her sources on the cards — friends, family, church cooks, a lady in the hospital, the Co-op paper. Here they are, as she named them.</p><div class="people">{rows}</div></div>'

def index_html():
    entries = []
    for r in recipes:
        titles = [r['title']]
        if ' / ' in (r['title'] or ''): titles += r['title'].split(' / ')
        for t in titles:
            t = t.strip()
            if not t: continue
            entries.append((t, r['id']))
    def sortkey(t): return re.sub(r'^(the|a|an)\s+', '', t.lower())
    entries.sort(key=lambda e: sortkey(e[0]))
    out = []; last = ''
    for t, rid in entries:
        L = sortkey(t)[:1].upper()
        if L != last:
            out.append(f'<div class="letter">{L}</div>'); last = L
        out.append(f'<div class="e"><a href="#r{rid}"><span class="t">{nice(t)}</span></a><span class="dots"></span><span class="p">{pg("r"+str(rid))}</span></div>')
    return blank_before('index') + f'<div class="back" id="index"><span class="pm">⟦index⟧</span><h2><span class="script">Index</span> of recipes</h2><div class="index">{"".join(out)}</div></div>'

def endnote_html():
    return f'<div class="endnote"><div class="art">{ILLOS["farm"]}</div><div class="script" style="font-size:22pt">Bake till done.</div><p style="font-style:italic;color:var(--pencil);margin-top:.2in">— Grandma</p></div>'

# ---------------------------------------------------------------- assemble
def build(screen=False):
    parts = []
    parts.append(f'<title>Grandma on the Farm</title><style>{CSS}{SCREEN_CSS if screen else ""}</style>')
    if screen: parts.append('<p class="webnote">Web edition — the printed book (PDF) carries full-size facsimiles; page numbers below refer to the printed book. Best viewed on a Mac or iPad, where the book’s typefaces are installed.</p><div class="page">')
    if screen: parts.append(cover_html())
    parts.append(front_matter(None))
    parts.append(toc_html())
    for k, t, illo in CHAPTERS:
        parts.append(chapter_html(k, t, illo, by_ch[k]))
    parts.append(chapter_html('extra', 'From the Front of the Box', 'broom', extras, extra=True).replace('<h2>From the Front of the Box</h2>', '<h2>From the Front of the Box</h2><p style="margin:-.05in 0 .05in;color:var(--pencil);font-style:italic;max-width:5.4in">Not everything in the box was a recipe. Tucked in front of the first divider were play-dough and bubble mixtures for the grandchildren, remedies, cleaning mixtures, a note on wasps, and the corn order for September 1991.</p>'))
    parts.append(people_html())
    parts.append(index_html())
    parts.append(endnote_html())
    if not screen and 'end' in BLANKS: parts.append('<div class="blankpage"></div>')
    if screen: parts.append('</div><a class="tocjump" href="#toc">Contents ↑</a>')
    return ''.join(parts)

def build_print_doc():
    return '<!doctype html><html lang="en"><head><meta charset="utf-8">' + build(screen=False).replace('<title>', '<title>', 1) + '</head><body></body></html>'

if __name__ == '__main__':
    mode = os.environ.get('MODE', 'print')
    if mode == 'print':
        body = build(screen=False)
        # move <title>+<style> to head
        mm = re.match(r'(<title>.*?</title><style>.*?</style>)(.*)$', body, re.S)
        doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8">{mm.group(1)}</head><body>{mm.group(2)}</body></html>'
        open(os.path.join(OUT, 'book.html'), 'w').write(doc)
        print('wrote', os.path.join(OUT, 'book.html'), len(doc))
    else:
        body = build(screen=True)
        open(os.path.join(OUT, 'book_web.html'), 'w').write(body)
        print('wrote', os.path.join(OUT, 'book_web.html'), len(body))
    # write data
    json.dump({'chapters': [{'key': k, 'title': t, 'recipes': [r['id'] for r in by_ch[k]]} for k, t, _ in CHAPTERS], 'recipes': recipes, 'extras': extras},
              open(os.path.join(OUT, 'recipes.json'), 'w'), ensure_ascii=False, indent=1)
