import sys, os
sys.argv = [sys.argv[0], os.path.dirname(os.path.abspath(__file__))]
import book
from illos import ILLOS
back = f'''<div class="cover back">
  <div class="frame"></div><div class="frame2"></div>
  <div class="blurb">
    <p>Behind the yellow tab dividers of a green metal recipe box — <span class="sc">Breads</span>, <span class="sc">Pies &amp; Pastries</span>, <span class="sc">Casseroles</span>, <span class="sc">Fish &amp; Seafoods</span>, <span class="sc">Preserves &amp; Jellies</span> — is a lifetime of feeding people: cinnamon buns for the breadmaker, four different Nanaimo bars, punches from the gas company and the church basement, saskatoon pie, cabbage rolls from a relative in Saskatchewan, and the play-dough recipe for the grandchildren.</p>
    <p>Every card in Grandma Harris’s box is here, transcribed exactly as she wrote it, with the original card alongside — her blue ballpoint, her shorthand, her “V.G.” in the corner.</p>
  </div>
  <div class="art2">{ILLOS['jars']}</div>
  <div class="foot">Bake till done.</div>
</div>'''
css = book.CSS + '''
@page bleedb { margin: 0; @bottom-center { content: none; } @top-left { content: none; } @top-right { content: none; } }
.cover.back { page: bleedb; break-before: page; }
.cover.back .blurb { position: absolute; top: 2.2in; left: 1.3in; right: 1.3in; font-size: 13pt; line-height: 1.55; text-align: center; }
.cover.back .blurb p { margin: 0 0 .35in; }
.cover.back .blurb .sc { letter-spacing: .1em; }
.cover.back .art2 { position: absolute; top: 6.6in; left: 3.1in; right: 3.1in; }
.cover.back .foot { font-family: "Snell Roundhand", cursive; text-transform: none; letter-spacing: 0; font-size: 20pt; bottom: 1.4in; }
'''
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Cover</title><style>{css}</style></head><body>{book.cover_html()}{back}</body></html>'
open(sys.argv[1] + '/cover.html', 'w').write(doc)
print('ok')
