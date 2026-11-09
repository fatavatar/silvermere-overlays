"""Writes the darkwood-quests overlay (the folder above this one): the Darkwood 8th and 9th
alignment quests, from the source package in `package/` (MajorMUD Explorer's columns), as a
silvermere content overlay.

The column translation is mme.py, checked against the whole realm by verify.py. What the
MDB does not carry comes from the realm: a new record starts from the realm record it was
modelled on (its messages, type and flags), and the six realm scripts the quests extend keep
their own links.

    REALM_DB=/path/to/silvermere.db SILVERMERE_SRC=/path/to/silvermere python3 source/convert.py

REALM_DB is a silvermere database holding the MudRev realm (stock plus the mudrev overlay will
do): new records start from realm records, and the realm scripts the quests extend keep their
links. SILVERMERE_SRC is a silvermere checkout (enums.py reads its code names).
"""
import os
import re
import sqlite3
import sys
from pathlib import Path

import tomli

import enums
import mme

HERE = Path(__file__).resolve().parent / 'package'
OUT = Path(__file__).resolve().parent.parent
if not os.environ.get('REALM_DB'):
    sys.exit('set REALM_DB to a silvermere database holding the MudRev realm')
REALM = sqlite3.connect(f"file:{os.environ['REALM_DB']}?mode=ro", uri=True)
DIRS = {'N': 'north', 'S': 'south', 'E': 'east', 'W': 'west', 'NE': 'northeast',
        'NW': 'northwest', 'SE': 'southeast', 'SW': 'southwest', 'U': 'up', 'D': 'down'}


def load(name):
    return tomli.load(open(HERE / f'{name}.toml', 'rb'))


# ---------------------------------------------------------------- TOML out

def q(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(int(v)) if float(v).is_integer() else repr(v)
    if isinstance(v, dict):
        return '{ ' + ', '.join(f'{key(k)} = {q(x)}' for k, x in v.items()) + ' }'
    if isinstance(v, (list, tuple)):
        return '[' + ', '.join(q(x) for x in v) + ']'
    s = str(v)
    if '\n' in s:
        return '"""\n' + s.replace('\\', '\\\\').replace('"""', '""\\"') + '"""'
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def key(k):
    return k if re.fullmatch(r'[A-Za-z0-9_-]+', k) else q(k)


def entry(kind, fields, comment=None):
    out = [f'# {comment}'] if comment else []
    out.append(f'[[{kind}]]')
    for k, v in fields.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            out.append(f'{key(k)} = [')
            out += [f'    {q(x)},' for x in v]
            out.append(']')
        else:
            out.append(f'{key(k)} = {q(v)}')
    return '\n'.join(out) + '\n'


def write(name, header, entries):
    OUT.joinpath(name).write_text('\n'.join(['\n'.join(f'# {h}' for h in header), ''] + entries))


# ---------------------------------------------------------------- translation

def named(field, code):
    return enums.name(mme.ENUMS[field], code) if field in mme.ENUMS else code


def plain(data, mapping):
    """The MME data columns as record fields; codes by name."""
    out = {}
    for col, f in mapping.items():
        if col in data and col != 'Name':
            out[f] = named(f, data[col])
    return out


def realm_attacks(n):
    return REALM.execute('select hitmsg,defmsg,missmsg from monster_attacks where monster=? '
                         'and kind!=0 order by slot', (n,)).fetchall()


def monster_attacks(data, template):
    """The attacks, each with the messages of the template's attack in the same place (the
    template's first one where it has fewer): the MDB carries no messages."""
    msgs = realm_attacks(template)
    out = []
    for i, a in enumerate(mme.attacks(data)):
        hit, dfm, miss = msgs[min(i, len(msgs) - 1)] if msgs else (0, 0, 0)
        if a['kind'] == 2:                      # a spell attack's messages are the spell's
            hit, dfm, miss = 1, 1, 1
        out.append(dict(kind=enums.name('MonsterAttackType', a['kind']), accuracy=a['accuracy'],
                        pct=a['pct'], min=a['min'], max=a['max'], energy=a['energy'],
                        hitspell=a['hitspell'], hitmsg=hit, defmsg=dfm, missmsg=miss))
    return out


def monsters():
    d = load('monsters')
    out = []
    for m in d.get('monster', []):
        data = m['data']
        f = dict(number=m['number'], **{'from': m['text_template']}, name=m['name'], desc=m['desc'])
        f.update(plain(data, mme.MONSTER))
        f['cash'] = {mme.MONSTER_CASH[c]: data.get(c, 0) for c in 'RPGSC'}
        f['abilities'] = [list(a) for a in m['abilities']]
        f['attacks'] = monster_attacks(data, m['text_template'])
        f['spells'] = mme.monster_spells(data)
        f['items'] = [dict(item=x['item'], uses=0, pct=x['pct']) for x in mme.drops(data)]
        out.append(entry('monster', f))
    for m in d.get('monster_change', []):
        f = dict(number=m['number'])
        if 'why' in m:
            f['why'] = m['why']
        f['set'] = {mme.MONSTER[k]: v for k, v in m['set'].items()}
        if 'desc' in m:
            f['set']['desc'] = m['desc']
        f['was'] = {mme.MONSTER[k]: v for k, v in m['was'].items()}
        out.append(entry('monster_change', f))
    write('monsters.toml', [
        'Monsters for the Darkwood 8th and 9th alignment quests (converted from',
        'source/package by source/convert.py; edit the source and convert again).',
        'A new monster starts from the realm monster it was modelled on and takes its attack',
        'messages; a change sets only its fields, and `was` is what the realm holds.'], out)


def items():
    d = load('items')
    out = []
    for it in d['item']:
        data = it.get('data', {})
        f = dict(number=it['number'], **{'from': it['text_template']}, name=it['name'], desc=it['desc'])
        f.update(plain(data, mme.ITEM))
        f['abilities'] = [list(a) for a in it.get('abilities', [])]
        for field, pre in (('classes', 'ClassRest-'), ('races', 'RaceRest-'), ('negates', 'NegateSpell-')):
            f[field] = mme.lists(data, pre)
        out.append(entry('item', f))
    write('items.toml', [
        'Items for the Darkwood quests: the three rewards, their upgrades, the rune, globe and',
        'glyph, and the mirror. Each starts from the realm item whose messages it borrows.'], out)


def spell_template(abilities, target):
    """A realm spell to start a new one from: its type, flags and resist settings, which the MDB
    does not carry. The realm's own quest plumbing for the plumbing spells; otherwise the first
    realm spell with the same first ability and target."""
    first = abilities[0][0] if abilities else 'None'
    if first == 'EndCast':
        return 1167
    if first == 'TextBlock':
        return 1168
    code = {v: k for k, v in enums.table('Ability').items()}[first]
    row = REALM.execute(
        'select s.number from spells s join spell_abilities a on a.spell=s.number and a.slot=0 '
        'where a.ability=? and s.target=? order by s.number limit 1', (code, target)).fetchone()
    row = row or REALM.execute(
        'select s.number from spells s join spell_abilities a on a.spell=s.number and a.slot=0 '
        'where a.ability=? order by s.number limit 1', (code,)).fetchone()
    return row[0] if row else 1168


def spells():
    d = load('spells')
    out = []
    for s in d['spell']:
        data = s.get('data', {})
        f = dict(number=s['number'], **{'from': spell_template(s['abilities'], data.get('Targets', 0))},
                 name=s['name'], msgnum=s['msgnum'], descs=s['desc'])
        # every column written, zeros too: a template lends only what the MDB lacks
        for col, field in mme.SPELL.items():
            if col not in ('Name', 'Short'):
                f[field] = named(field, data.get(col, 0))
        f['abilities'] = [list(a) for a in s['abilities']]
        out.append(entry('spell', f))
    write('spells.toml', [
        'Spells for the Darkwood quests. Most are plumbing: a monster\'s death spell ("temp")',
        'ends by casting a "text" spell that runs the quest step script.'], out)


# ---------------------------------------------------------------- rooms

def exit_value(text, here_map):
    """An exit in MME's notation (`3/790 (Door [1000 picklocks/strength])`, `1/1`) as the
    record holds it: a lockable door is a gate exit, locked, that cannot be picked; another
    map is a map-change exit naming the map."""
    m = re.match(r'(\d+)/(\d+)\s*(.*)$', text)
    dest_map, dest, rest = int(m[1]), int(m[2]), m[3]
    if 'Door' in rest:
        return dict(target=dest, kind='Gate', par1=2, par2=-999)
    if dest_map != here_map:
        return dict(target=dest, kind='MapChange', par1=dest_map)
    if rest:
        raise ValueError(f'exit {text!r}: not translated')
    return dest


ROOM_FIELD = {'NPC': 'specmon', 'CMD': 'cmdtext', 'Spell': 'roomspell'}


def room_values(data):
    out = {}
    for k, v in data.items():
        if k == 'Placed':
            out['placed'] = [int(x) for x in str(v).split(',') if x.strip()]
        else:
            out[ROOM_FIELD[k]] = v
    return out


def rooms():
    d = load('rooms')
    out = []
    for r in d['room']:
        f = dict(map=r['map'], room=r['room'], name=r['name'], desc=r['desc'])
        f['exits'] = {DIRS[k]: exit_value(v, r['map']) for k, v in r.get('exits', {}).items()}
        f.update(room_values(r.get('data', {})))
        out.append(entry('room', f, 'fills a realm "Buffer Room" placeholder'))
    for r in d['room_change']:
        f = dict(map=r['map'], room=r['room'])
        if 'why' in r:
            f['why'] = r['why']
        f['set'] = room_values(r['set'])
        f['was'] = room_values(r['was'])
        out.append(entry('room_change', f))
    write('rooms.toml', [
        'Rooms for the Darkwood quests: the false King\'s throne room behind the mirror and the',
        'void beyond its door (both fill realm placeholders), and the realm rooms they change.'], out)


# ---------------------------------------------------------------- text

MARKUP = [('{k}', '{ansi:1;32}'), ('{/k}', '{ansi:0;32}'), ('{hint}', '{ansi:1;33}'),
          ('{/hint}', '{ansi:0;32}'),
          ('{exp}', '{ansi:0;36}<You gain 3,000,000,000 experience!>{ansi:0;32}')]


def prose(text):
    """The drafts' markup in the realm's colours: speech green, keywords bright green, the goal
    line yellow, the experience line cyan."""
    t = text.replace('{', '\x00').replace('}', '\x01')
    for a, b in MARKUP:
        t = t.replace(a.replace('{', '\x00').replace('}', '\x01'), b)
    t = t.replace('\x00', '{{').replace('\x01', '}}')
    return '{ansi:0;32}' + t.rstrip('\n') + '{ansi:0}\n'


def scripts_and_text():
    d = load('scripts')
    t = load('text')
    out = []
    for s in d['script_change']:
        link = REALM.execute('select link from text_blocks where number=? and part=0',
                             (s['number'],)).fetchone()[0]
        out.append(entry('text', dict(
            number=s['number'], replace=True, link=link, text=s['action'],
            why=f"{s['who']}: the realm's lines plus {', '.join(s['added'])}")))
    for s in d['script']:
        out.append(entry('text', dict(number=s['number'], link=s.get('leads_to', 0), text=s['action'])))
    # A prose block's link is the block it leads on to: the one that names it as its caller.
    # (A script's callers are its topics, reached by keyword, not by link.)
    prose_numbers = {p['number'] for p in t['text']}
    link_of = {}
    for b in d['script'] + t['text']:
        m = re.fullmatch(r'Textblock #(\d+)', b.get('called_from', ''))
        if m and int(m[1]) in prose_numbers:
            link_of[int(m[1])] = b['number']
    for p in t['text']:
        out.append(entry('text', dict(number=p['number'], link=link_of.get(p['number'], 0),
                                      text=prose(p['text']))))
    write('text.toml', [
        'The Darkwood quest scripts (word for word from the MDB), the six realm scripts they',
        'extend (taken over whole with `replace = true`, keeping their links), and the drafted',
        'conversations.'], out)


def messages():
    d = load('messages')
    out = [entry('message', dict(number=m['number'], msgs=[m['text0'], m['text1'], m['text2']]))
           for m in d['message']]
    write('messages.toml', ['New messages: line 1 to the one acting, line 2 to the target, line 3',
                            'to the room.'], out)


OUT.mkdir(parents=True, exist_ok=True)
OUT.joinpath('overlay.toml').write_text(
    'name = "darkwood-quests"\n'
    'description = "The Darkwood 8th and 9th alignment quests (levels 150 and 200), converted '
    'from source/package by source/convert.py."\n'
    'after = ["mudrev"]\n')
monsters()
items()
spells()
rooms()
scripts_and_text()
messages()
print('wrote', OUT)
