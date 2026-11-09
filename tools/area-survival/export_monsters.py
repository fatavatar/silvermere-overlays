"""Monsters as a world holds them now (after overlays), for zone.mjs: the fields MME's model
reads, in silvermere's names, plus each monster's attacks and abilities (as codes).

    python3 export_monsters.py DB N... > monsters.json
"""
import json, sqlite3, sys

db = sqlite3.connect(f'file:{sys.argv[1]}?mode=ro', uri=True)
out = {}
for n in map(int, sys.argv[2:]):
    r = db.execute('select name,maxhp,ac,dr,magicres,exp,level,energy,hpregen,regenhrs,bsdefense '
                   'from monsters where number=?', (n,)).fetchone()
    if not r:
        continue
    att = [dict(zip(('kind', 'accuracy', 'pct', 'min', 'max', 'energy', 'hitspell'), a)) for a in db.execute(
        'select kind,accuracy,pct,min,max,energy,hitspell from monster_attacks where monster=? order by slot', (n,))]
    abil = [list(a) for a in db.execute(
        'select ability,value from monster_abilities where monster=? order by slot', (n,))]
    out[n] = dict(zip(('name', 'maxhp', 'ac', 'dr', 'magicres', 'exp', 'level', 'energy', 'hpregen',
                       'regenhrs', 'bsdefense'), r), attacks=att, abilities=abil)
json.dump(out, sys.stdout)
