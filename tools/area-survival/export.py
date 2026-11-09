"""Input for survive.mjs: our characters (level > 40) and every area's spawn pool.

An area is the rooms on one map sharing a name up to the first comma. Its pool is what the engine
would spawn there: monsters whose montype is the room's mongroup and whose genindex is in the
room's minlevel..maxlevel, plus the room's genmonster, weighted by the rooms that can spawn them.

    python3 export.py silvermere.db > input.json
    node survive.mjs input.json output.json
"""
import json, sqlite3, sys
from collections import defaultdict

if len(sys.argv) < 2:
    sys.exit('usage: export.py SILVERMERE_DB > input.json')
path = sys.argv[1]
db = sqlite3.connect(f'file:{path}?mode=ro', uri=True)

chars = []
for cid, name, lv, cl, rc, s, i, w, a, h, c, wpn in db.execute(
        'select id,firstname,level,class,race,basstr,basint,baswil,basagi,bashea,bascha,weapon '
        'from characters where level > 40'):
    worn = [it for (it,) in db.execute('select item from character_worn where character_id=? and item!=0', (cid,))]
    spells = [sp for (sp,) in db.execute('select spell from character_spellbook where character_id=? and spell!=0', (cid,))]
    chars.append(dict(name=name, level=lv, cls=cl, race=rc, weapon=wpn, worn=worn, spells=spells,
                      stats=dict(str=s, int=i, wis=w, agi=a, hea=h, cha=c)))

bygen = defaultdict(list)
for n, t, g in db.execute('select number,montype,genindex from monsters'):
    bygen[(t, g)].append(n)
areas = defaultdict(lambda: {'rooms': 0, 'mons': defaultdict(int), 'spec': set()})
for m, name, mn, mx, grp, gm, spec in db.execute(
        'select map,name,minlevel,maxlevel,mongroup,genmonster,specmon from rooms'):
    a = areas[f'{m}|{name.split(",")[0].strip()}']
    a['rooms'] += 1
    if mx:
        for (t, g), ns in bygen.items():
            if (grp == -1 or t == grp) and (mn == 0 or g >= mn) and g <= mx:
                for n in ns: a['mons'][n] += 1
    if gm: a['mons'][gm] += 1
    if spec: a['spec'].add(spec)
out = {k: {'rooms': a['rooms'], 'mons': dict(a['mons']), 'spec': sorted(a['spec'])}
       for k, a in areas.items() if a['rooms'] >= 10 and a['mons']}
json.dump({'chars': chars, 'areas': out}, sys.stdout)
