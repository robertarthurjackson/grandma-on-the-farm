import json,re
allp=json.load(open('../all_photos.json'))
DUPES={67,174,349,360,362,364,368,370}
DIVIDERS={0:'BOX',93:'Breads',228:'Pies & Pastries',273:'Casseroles',308:'Desserts & Puddings',330:'Slices & Bars',356:'Eggs & Cheese',372:'Fish & Seafoods',403:'Frostings & Fillings',418:"Hors d'Oeuvres",423:'Meats',459:'Poultry & Stuffings',482:'Preserves & Jellies',502:'Salads & Dressings',552:'Sandwiches',555:'Sauces',561:'Soups & Stews',588:'Vegetables',606:'Miscellaneous'}
def section_of(n):
    s='Front of the Box'
    for k in sorted(DIVIDERS):
        if n>=k and k>0: s=DIVIDERS[k]
    return s
recipes=[]; extras=[]; cur=None
for e in allp:
    n=e['photo']
    if n in DUPES or n in DIVIDERS or n==55: continue
    if e['kind']=='continuation':
        if cur is None: continue
        cur['photos'].append(n)
        cur['ingredients']+=e['ingredients']; cur['directions']+=e['directions']
        cur['notes']+=[x for x in e['notes'] if x not in cur['notes']]
        cur['raw_text']+='\n[back]\n'+e['raw_text']
        if e['confidence']=='medium': cur['confidence']='medium'
        continue
    r={'id':n,'photos':[n],'title':e['title'],'attribution':e['attribution'],'agent_category':e['category'],
       'ingredients':list(e['ingredients']),'directions':list(e['directions']),'notes':list(e['notes']),
       'kind':e['kind'],'section':section_of(n),'confidence':e['confidence'],'multiple_cards':e['multiple_cards'],'raw_text':e['raw_text']}
    cur=r
    if e['kind'] in ('recipe','clipping'): recipes.append(r)
    else: extras.append(r)
json.dump({'recipes':recipes,'extras':extras},open('merged.json','w'),ensure_ascii=False,indent=1)
print(len(recipes),len(extras))
import collections
print(collections.Counter(r['section'] for r in recipes))
