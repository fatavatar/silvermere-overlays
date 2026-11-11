"""Writes ../rooms.toml: the Gilded Asylum's rooms on map 20, and the way up from the Padded
Cell on map 9.

The layout is drawn here as grids and chains so the exits always pair up; the room kinds
(name, description, spawns) are in KINDS. Run it after changing either:

    python3 source/rooms.py
"""
import textwrap
from pathlib import Path

MAP = 20
CELL = (9, 1255)          # Padded Cell: its only exit is north
CRAWL = (9, 1500)         # a new room on map 9 above the cell: a text exit cannot change maps
GROUP = 'Group28'         # monster group 33, which no realm monster uses
DIRS = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west', 'u': 'up', 'd': 'down',
        'ne': 'northeast', 'nw': 'northwest', 'se': 'southeast', 'sw': 'southwest'}
BACK = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u',
        'ne': 'sw', 'sw': 'ne', 'nw': 'se', 'se': 'nw'}

# Generation index by spawn tier (monsters.toml): 1 treated lunatic, 2 mirror-patient,
# 3 orderly, 4 treated murderer, 5 animated straitjacket, 6 warden.
KINDS = {
    'landing': dict(
        name='Gilded Asylum, Attic Landing',
        desc="""You climb out of the crawlspace onto bare boards. Behind a rotted screen
        the attic opens into a landing hung with velvet, and every nail, hinge and
        picture frame has been gilded. The gold is very new. The plaster under it is
        cracked and stained, and somewhere ahead someone is laughing at nothing."""),
    'corridor': dict(
        name='Gilded Asylum, Gilded Corridor',
        desc="""A long corridor runs between doors with small barred windows. The
        floorboards have been gilded too, and they ring dully underfoot like coins.
        Brass plates by each door name a treatment rather than a patient: COLD BATHS,
        LEECHING, THE QUIETING DRAUGHT. Most of the doors stand open."""),
    'rotunda': dict(
        name='Gilded Asylum, Rotunda',
        desc="""The corridors meet under a dome painted with a sky of gold stars. A
        marble statue of a physician stands in the centre, one hand raised in blessing
        and the other holding a cup; someone has filled the cup with teeth. Signs point
        to the wards of Whispers, Fevers and Chains, and a fourth, newer sign points down
        a stair to THE LABORATORY - STAFF ONLY."""),
    'dispensary': dict(
        name='Gilded Asylum, Dispensary',
        desc="""Shelves of stoppered bottles line this narrow room, each one labelled in a
        neat and careful hand. A heavy table has been pushed against the door to the
        wards, and behind it a lamp burns low over a mortar, a pestle and an open
        ledger. It is the only room you have seen that nobody has gilded."""),
    'whispers': dict(
        name='Gilded Asylum, Ward of Whispers',
        desc="""Rows of iron beds stand under white sheets in a long, dim ward. The
        sheets move, though there is no draught, and from every side comes a soft,
        constant whispering that stops whenever you turn towards it. Mirrors have been
        hung over every bed, angled so that each patient could only ever see itself.""",
        spawn=(1, 3), max=2),
    'whisper_gallery': dict(
        name='Gilded Asylum, Whispering Gallery',
        desc="""The ward ends in a round gallery lined with mirrors from floor to dome.
        Your reflection stands in every one of them, but not all of the reflections are
        moving with you. A pale woman sits on a gilded throne in the centre, combing hair
        as white as snow, and every mirror whispers when she speaks."""),
    'fevers': dict(
        name='Gilded Asylum, Ward of Fevers',
        desc="""Heat beats out of this ward like an open oven. Braziers burn between the
        beds, and the walls have blistered and peeled under their gilding. Patients were
        brought here to have fevers sweated out of them; from the scorch marks on the
        straps, the treatment went on long after the fevers stopped.""",
        spawn=(3, 4), max=2),
    'furnace': dict(
        name='Gilded Asylum, Furnace Room',
        desc="""A great iron furnace fills the end of the fever ward, its door hanging
        open on a bed of white coals. The air ripples with heat and the floor is too hot
        to stand on for long. A woman in a burning gown tends the coals with her bare
        hands, singing to them softly, and does not look up."""),
    'chains': dict(
        name='Gilded Asylum, Ward of Chains',
        desc="""This ward held the violent ones. Every bed is bolted to the floor and
        hung with gilded chains, and the walls are scored with deep gouges at the height
        of a man's shoulders. Many of the chains have been snapped. A few have not, and
        whatever they held is no longer in them.""",
        spawn=(4, 6), max=2),
    'iron_cell': dict(
        name='Gilded Asylum, Iron Cell',
        desc="""The last cell of the ward is lined with iron plate and has no window. Its
        door has been torn from the hinges and thrown across the corridor. Inside, a
        huge figure squats among broken chains, wearing the twisted remains of a
        restraint collar as if it were a crown."""),
    'stair': dict(
        name='Gilded Asylum, Laboratory Stair',
        desc="""A spiral stair of gilded iron winds down into the dark below the
        rotunda. The steps are worn in the middle by many feet, and the brass handrail
        is sticky. A sharp chemical smell rises from below, and with it the sound of
        two voices arguing, very calmly, about the colour of pain."""),
    'sorcerer': dict(
        name="Gilded Asylum, Sorcerer's Landing",
        desc="""The stair opens onto a landing hung with star charts, every one of them
        wrong. A gaunt man in a robe sewn with tiny mirrors stands at a lectern, writing
        in a book with no pages. He looks up as you arrive and smiles with far too many
        teeth."""),
    'magus': dict(
        name="Gilded Asylum, Magus's Landing",
        desc="""The landing narrows before a pair of gilded doors, sealed with a lock in
        the shape of an open mouth. A hunched figure in scholar's robes paces before
        them, counting his own fingers over and over and never reaching the same
        number twice."""),
    'laboratory': dict(
        name="Gilded Asylum, Shrefwan's Laboratory",
        desc="""Tables crowded with glassware fill a long vaulted cellar. Alembics bubble
        over blue flames, copper pipes run along the ceiling and drip into pans of
        gilding, and jars of floating things line every wall. In the far corner a
        cabinet of black wood stands open, its shelves bright with stolen treasures."""),
    'sanctum': dict(
        name='Gilded Asylum, Alchemical Sanctum',
        desc="""The laboratory ends in a round chamber around a vat of liquid gold, kept
        molten by a ring of furnaces. A thin old man in a gilded apron stands on its rim,
        sipping from a beaker that smokes. His skin has begun to shine like the metal in
        the vat, and his eyes have no whites left at all."""),
}

rooms = {}        # number -> dict(kind, exits {dir: target})
order = []
coords = {}       # number -> (x, y) for rooms laid out on a grid


def room(n, kind):
    rooms[n] = dict(kind=kind, exits={})
    order.append(n)


def link(a, d, b):
    assert d not in rooms[a]['exits'], (a, d)
    assert BACK[d] not in rooms[b]['exits'], (b, BACK[d])
    rooms[a]['exits'][d] = b
    rooms[b]['exits'][BACK[d]] = a


def grid(first, w, h, kind_at, holes=()):
    """Rooms numbered row by row from `first`; returns {(x, y): number}."""
    cells, n = {}, first
    for y in range(h):
        for x in range(w):
            if (x, y) in holes:
                continue
            cells[(x, y)] = n
            coords[n] = (x, y)
            room(n, kind_at(x, y))
            n += 1
    for (x, y), a in cells.items():
        if (x + 1, y) in cells:
            link(a, 'e', cells[(x + 1, y)])
        if (x, y + 1) in cells:
            link(a, 's', cells[(x, y + 1)])
    return cells


# the landing and the corridor south to the rotunda
room(1, 'landing')
corridor = [2, 3, 4]
for n in corridor:
    room(n, 'corridor')
link(1, 's', 2)
link(2, 's', 3)
link(3, 's', 4)
rotunda = 5
room(rotunda, 'rotunda')
link(4, 's', rotunda)
dispensary = 6
room(dispensary, 'dispensary')
link(rotunda, 'se', dispensary)

# the Ward of Whispers west of the rotunda, 5 x 4, the gallery at its far end
whispers = grid(7, 5, 4, lambda x, y: 'whispers', holes={(1, 1), (3, 2)})
link(rotunda, 'w', whispers[(4, 1)])
gallery = max(rooms) + 1
room(gallery, 'whisper_gallery')
link(whispers[(0, 2)], 'w', gallery)

# the Ward of Fevers east of the rotunda, 5 x 4, the furnace room at its far end
nxt = max(rooms) + 1
fevers = grid(nxt, 5, 4, lambda x, y: 'fevers', holes={(2, 0), (1, 3)})
link(rotunda, 'e', fevers[(0, 1)])
furnace = max(rooms) + 1
room(furnace, 'furnace')
link(fevers[(4, 2)], 'e', furnace)

# the Ward of Chains north-east of the corridor, 5 x 5, the iron cell at its far end
nxt = max(rooms) + 1
chains = grid(nxt, 5, 5, lambda x, y: 'chains', holes={(2, 2), (0, 4), (4, 0)})
link(3, 'e', chains[(0, 2)])
cell = max(rooms) + 1
room(cell, 'iron_cell')
link(chains[(4, 2)], 'e', cell)

# the laboratory below the rotunda: the stair, the two landings, the doors, the laboratory
stair = max(rooms) + 1
room(stair, 'stair')
room(stair + 1, 'stair')
link(rotunda, 'd', stair)
link(stair, 'd', stair + 1)
sorcerer = stair + 2
room(sorcerer, 'sorcerer')
link(stair + 1, 's', sorcerer)
magus = sorcerer + 1
room(magus, 'magus')
link(sorcerer, 's', magus)
lab = magus + 1
room(lab, 'laboratory')
room(lab + 1, 'laboratory')
link(magus, 's', lab)
link(lab, 's', lab + 1)
sanctum = lab + 2
room(sanctum, 'sanctum')
link(lab + 1, 'e', sanctum)

SPECIAL = {
    dispensary: dict(specmon=2119),
    gallery: dict(specmon=2116),
    furnace: dict(specmon=2115),
    cell: dict(specmon=2117),
    sorcerer: dict(specmon=1386),
    magus: dict(specmon=1387),
    sanctum: dict(specmon=1385),
}
# Every ward room is a lair: the wards are full, as an asylum's wards are.
LAIR = {'whispers', 'fevers', 'chains'}

# the laboratory doors: locked, opened by the gilded key, not pickable
DOOR = dict(kind='Key', par1=5113, par2=2, par3=-999, par4=1)


def wrap(text, width=70, lines=7):
    out = textwrap.wrap(' '.join(text.split()), width)
    assert len(out) <= lines, (text[:40], len(out))
    return out


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


out = ['# Generated by source/rooms.py; edit that and run it again.', '',
       '[defaults.room]', 'regendelay = 5', '']
for n in order:
    r, k = rooms[n], KINDS[rooms[n]['kind']]
    out += ['[[room]]', f'map = {MAP}', f'room = {n}', f'name = {q(k["name"])}',
            'desc = """\n' + '\n'.join(wrap(k['desc'])) + '\n"""']
    exits = []
    for d, t in sorted(r['exits'].items(), key=lambda kv: list(DIRS).index(kv[0])):
        if {n, t} == {magus, lab}:
            exits.append(f'{DIRS[d]} = {{ target = {t}, kind = "Key", par1 = {DOOR["par1"]}, '
                         f'par2 = {DOOR["par2"]}, par3 = {DOOR["par3"]}, par4 = {DOOR["par4"]} }}')
        else:
            exits.append(f'{DIRS[d]} = {t}')
    if n == 1:
        exits.insert(0, f'down = {{ target = {CRAWL[1]}, kind = "MapChange", par1 = {CRAWL[0]} }}')
    out.append('exits = { ' + ', '.join(exits) + ' }')
    if 'spawn' in k:
        out.append('room_type = "Lair"')
        out += [f'mongroup = 33', f'minlevel = {k["spawn"][0]}', f'maxlevel = {k["spawn"][1]}',
                f'maxmonsters = {k["max"]}']
    for f, v in SPECIAL.get(n, {}).items():
        out.append(f'{f} = {q(v) if isinstance(v, str) else v}')
    out.append('')

crawl = dict(
    name='Padded Cell, Crawlspace',
    desc="""Above the padded cell the ceiling panel opens onto a crawlspace between the
    joists, thick with dust and old horsehair. A faint golden light shows through the
    boards overhead, and you can hear footsteps up there, pacing, always pacing.""")
out += ['# The crawlspace above the Padded Cell: a text exit cannot change maps, so the panel',
        '# leads to this room on map 9, and it climbs up to the asylum.',
        '[[room]]', f'map = {CRAWL[0]}', f'room = {CRAWL[1]}', f'name = {q(crawl["name"])}',
        'desc = """\n' + '\n'.join(wrap(crawl['desc'])) + '\n"""',
        f'exits = {{ up = {{ target = 1, kind = "MapChange", par1 = {MAP} }}, '
        f'down = {CELL[1]} }}', '',
        '# The way in: the Padded Cell gets a loose ceiling panel ("climb panel").',
        '[[room_change]]', f'map = {CELL[0]}', f'room = {CELL[1]}',
        'why = "the way up into the Gilded Asylum: a text exit, climb panel"',
        f'set = {{ exits = {{ up = {{ target = {CRAWL[1]}, kind = "Text", par1 = 10330, '
        f'par3 = 10331, par4 = 10332 }} }}, desc = """\n'
        + '\n'.join(wrap("""The walls of this small, square room once were padded with thick cloth
        mats. Now, however, they have been torn to shreds and in many places are stained
        with dark spots that look suspiciously like blood. One panel of the ceiling hangs
        loose, and a faint golden light shows around its edges.""")) + '\n""" }',
        'was = { name = "Padded Cell" }', '']
Path(__file__).resolve().parent.parent.joinpath('rooms.toml').write_text('\n'.join(out))
print(len(order) + 1, 'rooms; dispensary', dispensary, 'gallery', gallery, 'furnace', furnace,
      'cell', cell, 'sorcerer', sorcerer, 'magus', magus, 'lab', lab, 'sanctum', sanctum)
