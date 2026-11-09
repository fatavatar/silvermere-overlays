"""Checks mme.py against the realm: every record mudtool's export of mudrev.mdb and the realm
database both hold, translated field by field. Prints how often each field disagrees."""
import json, os, sqlite3
from collections import Counter
import mme

# REALM_DB: the realm as imported, before any overlay; MUDTOOL_DATA: mudtool's export of the
# realm's MME database (data/*.json)
DB = sqlite3.connect(f"file:{os.environ['REALM_DB']}?mode=ro", uri=True)
DB.row_factory = sqlite3.Row


def rows(t):
    d = json.load(open(os.path.join(os.environ['MUDTOOL_DATA'], f'{t}.json')))
    return {r[0]: dict(zip(d['cols'], r)) for r in d['rows']}


def check(table, mapping, key='number', extra=None):
    bad, seen = Counter(), 0
    for n, r in rows(table).items():
        rec = DB.execute(f'select * from {table} where {key}=?', (n,)).fetchone()
        if not rec:
            continue
        seen += 1
        for col, f in mapping.items():
            if r.get(col) is None:
                continue
            got = rec[mme.COLUMN.get(f, f)]
            want = r[col]
            if isinstance(want, float):
                want = int(want)
            if f == 'name':
                got, want = got.strip(), str(want).strip()
            if got != want:
                bad[f] += 1
        if extra:
            for f in extra(n, r):
                bad[f] += 1
    print(f'{table}: {seen} records; disagreements:', dict(bad.most_common()) or 'none')


def monster_extra(n, r):
    out = []
    ab = [(a, v) for a, v in DB.execute('select ability,value from monster_abilities where monster=? and ability!=0 order by slot', (n,))]
    if sorted(ab) != sorted(mme.abilities(r, 10)):
        out.append('abilities')
    at = [dict(x) for x in DB.execute('select kind,accuracy,pct,min,max,energy,hitspell from monster_attacks where monster=? and kind!=0 order by slot', (n,))]
    if at != mme.attacks(r):
        out.append('attacks')
    sp = [dict(x) for x in DB.execute('select spell,pct,level from monster_spells where monster=? order by slot', (n,))]
    if [s for s in sp if s['spell'] or s['pct']] != mme.monster_spells(r):
        out.append('spells')
    it = [dict(x) for x in DB.execute('select item,pct from monster_items where monster=? and item!=0 order by slot', (n,))]
    if it != mme.drops(r):
        out.append('items')
    cash = DB.execute('select cash_runic,cash_platinum,cash_gold,cash_silver,cash_copper from monsters where number=?', (n,)).fetchone()
    if list(cash) != [r[c] for c in 'RPGSC']:
        out.append('cash')
    return out


def item_extra(n, r):
    out = []
    ab = list(DB.execute('select ability,value from item_abilities where item=? and ability!=0 order by slot', (n,)))
    if sorted(map(tuple, ab)) != sorted(mme.abilities(r, 20)):
        out.append('abilities')
    for t, col, pre in [('item_classes', 'class', 'ClassRest-'), ('item_races', 'race', 'RaceRest-'), ('item_negates', 'spell', 'NegateSpell-')]:
        got = [x[0] for x in DB.execute(f'select {col} from {t} where item=? and {col}!=0 order by slot', (n,))]
        if got != mme.lists(r, pre):
            out.append(t)
    return out


def spell_extra(n, r):
    ab = list(DB.execute('select ability,value from spell_abilities where spell=? and ability!=0 order by slot', (n,)))
    return [] if sorted(map(tuple, ab)) == sorted(mme.abilities(r, 10)) else ['abilities']


check('monsters', mme.MONSTER, extra=monster_extra)
check('items', mme.ITEM, extra=item_extra)
check('spells', mme.SPELL, extra=spell_extra)
