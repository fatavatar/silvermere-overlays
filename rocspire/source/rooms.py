"""Writes ../rooms.toml: the Rocspire's rooms on map 21 and the way up from Gloomy Mountain's
Pinnacle.

The layout is drawn here as grids and chains so the exits always pair up; the room kinds
(name, description, spawns) are in KINDS. Run it after changing either:

    python3 source/rooms.py
"""
import textwrap
from pathlib import Path

MAP = 21
ENTRANCE = (3, 5661)      # Gloomy Mountain, Pinnacle: the starmetal giant king's lair, only exit down
GROUP = 34                # monster group 34 (Group29), which no realm monster uses
DIRS = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west', 'u': 'up', 'd': 'down',
        'ne': 'northeast', 'nw': 'northwest', 'se': 'southeast', 'sw': 'southwest'}
BACK = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u',
        'ne': 'sw', 'sw': 'ne', 'nw': 'se', 'se': 'nw'}

# Generation index by spawn tier (monsters.toml): 1 hawk swarm, 2 nomad raider, 3 frost-pelt
# shaman, 4 nomad huntmaster, 5 roc broodling, 6 giant roc, 7 storm elemental.
KINDS = {
    'bridge': dict(
        name='Rocspire, Rope Bridge',
        desc="""A bridge of rope and weathered planks sways over a drop you cannot see the
        bottom of. The wind howls between the spires and tears at your clothes, and every
        gust swings the bridge out over nothing. Old roc feathers, each as long as a
        spear, are knotted into the ropes as charms.""",
        spawn=(1, 2), max=1, light=-60),
    'ledge': dict(
        name='Rocspire, Windswept Ledge',
        desc="""A narrow ledge of grey rock winds around the face of a spire, scoured smooth
        by the wind. Below, clouds pour between the peaks like a slow white river. The rock
        is streaked white with droppings, and long scratches score it where something with
        great claws has landed.""",
        spawn=(1, 2), max=2, light=-60),
    'camp': dict(
        name='Rocspire, Nomad Camp',
        desc="""Tents of stitched white pelts crowd a sheltered saddle between two spires,
        their guy-ropes weighted with stones against the wind. Smoke rises from fire-pits,
        and racks of roc meat dry in the cold air. Men and women in white furs watch you
        from every doorway, and none of them look friendly.""",
        spawn=(2, 4), max=2),
    'longhall': dict(
        name='Rocspire, the Longhall',
        desc="""A hall of black timber runs the length of the saddle, its roof beams carved
        with rocs in flight. A fire burns down the middle of it in a long stone trench, and
        benches line the walls under hanging shields. The air is thick with smoke, ale and
        old songs."""),
    'hearth': dict(
        name='Rocspire, Saga Hearth',
        desc="""At the end of the Longhall a small fire burns in a round hearth, and an old
        woman sits beside it with her hands folded in her lap. Her eyes are milk white. The
        walls around her are hung with knotted cords, hundreds of them, each knot a deed
        and each cord a life."""),
    'throne': dict(
        name="Rocspire, Jarl's High Seat",
        desc="""A raised seat of roc bone stands at the head of the Longhall, draped in a
        white pelt larger than any bear's. A broad man with a beard braided with gold rises
        from it as you approach, a heavy axe in one hand and a drinking horn in the
        other."""),
    'champion': dict(
        name="Rocspire, Champion's Ring",
        desc="""A ring of stones has been set into the Longhall's floor before the high
        seat, the ground inside it trampled hard and dark with old blood. A lean warrior in
        lacquered armour from some far country waits inside it, a long curved sword resting
        across her knees."""),
    'nest': dict(
        name='Rocspire, Roc Nests',
        desc="""Great nests of whole trees and bones crown the spires here, each one as wide
        as a house. The ground between them is a slope of broken eggshell and droppings, and
        the air is full of the screaming of hungry chicks. Overhead, a shadow passes, and
        then another.""",
        spawn=(5, 6), max=2),
    'eyrie': dict(
        name='Rocspire, Eyrie',
        desc="""A shelf of rock juts out from the spire into empty air, its edge worn smooth
        by the landing of enormous claws. Bones lie scattered everywhere: deer, horses,
        oxen, and some that once wore armour. The wind here smells of blood.""",
        spawn=(5, 6), max=2),
    'matriarch': dict(
        name="Rocspire, Matriarch's Nest",
        desc="""The highest nest of all is woven from whole pines and the ribs of ships. Eggs
        the size of wagons lie in it, warm under a blanket of white down, and over them
        crouches a roc so vast that her folded wings make a roof against the sky. She opens
        one golden eye."""),
    'stair': dict(
        name='Rocspire, Stormcrown Stair',
        desc="""Steps have been cut into the side of the highest spire, spiralling up into the
        storm. Lightning flickers in the clouds around you, close enough to raise the hair on
        your arms, and the rock hums underfoot. Shapes of living lightning drift between the
        flashes.""",
        spawn=(6, 7), max=1, light=-60),
    'crown': dict(
        name='Rocspire, Stormcrown',
        desc="""The top of the highest spire is a ring of standing stones blackened by
        lightning. The storm is everywhere here: above, below, and in the air between the
        stones, which crackles and snaps. Shapes of living lightning circle the ring,
        watching.""",
        spawn=(7, 7), max=2),
    'bell': dict(
        name='Rocspire, Storm-Bell',
        desc="""In the centre of the stone ring hangs a great bell of black iron, green with age,
        from a frame of roc bone. Its clapper is chained up and wrapped in pelts. Knotted cords
        hang from the frame, and the saga-keeper's people say that whoever rings it is heard
        by every ancestor at once."""),
}

rooms = {}        # number -> dict(kind, exits {dir: target})
order = []
coords = {}


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


def chain(first, kind, dirs):
    """len(dirs)+1 rooms from `first`, each linked to the next by the next direction."""
    ns = list(range(first, first + len(dirs) + 1))
    for n in ns:
        room(n, kind)
    for a, b, d in zip(ns, ns[1:], dirs):
        link(a, d, b)
    return ns


# the rope bridges: a chain of 12 swaying north and east from the Pinnacle
bridge = chain(1, 'bridge', ['n', 'n', 'ne', 'n', 'e', 'e', 'ne', 'n', 'n', 'nw', 'n'])

# the windswept ledges around the spires, 7 x 4
nxt = max(rooms) + 1
ledges = grid(nxt, 7, 4, lambda x, y: 'ledge', holes={(3, 1), (5, 2)})
link(bridge[-1], 'n', ledges[(0, 3)])

# the nomad camp east of the ledges, 5 x 5, and the Longhall beyond
nxt = max(rooms) + 1
camp = grid(nxt, 5, 5, lambda x, y: 'camp', holes={(2, 2)})
link(ledges[(6, 1)], 'e', camp[(0, 1)])
hall = chain(max(rooms) + 1, 'longhall', ['e', 'e', 'e'])
link(camp[(4, 2)], 'e', hall[0])
hearth = max(rooms) + 1
room(hearth, 'hearth')
link(hall[1], 'n', hearth)
ring = hearth + 1
room(ring, 'champion')
link(hall[-1], 'e', ring)
throne = ring + 1
room(throne, 'throne')
link(ring, 'e', throne)

# the roc nests north of the ledges, 9 x 5, eyries on the edges; the Matriarch above them
nxt = max(rooms) + 1
nests = grid(nxt, 9, 5, lambda x, y: 'eyrie' if y in (0, 4) and x % 3 == 0 else 'nest',
             holes={(4, 2)})
link(ledges[(3, 0)], 'n', nests[(3, 4)])
matriarch = max(rooms) + 1
room(matriarch, 'matriarch')
link(nests[(8, 0)], 'u', matriarch)

# the Stormcrown: a stair of 28 winding up from the nests, the crown's ring, the bell
stair_dirs = ['u', 'n', 'u', 'e', 'u', 's', 'u', 'e', 'u', 'n', 'u', 'w', 'u', 'n',
              'u', 'e', 'u', 's', 'u', 'e', 'u', 'n', 'u', 'w', 'u', 'n', 'u']
stair = chain(max(rooms) + 1, 'stair', stair_dirs)
link(nests[(0, 0)], 'u', stair[0])
nxt = max(rooms) + 1
crown = grid(nxt, 3, 2, lambda x, y: 'crown')
link(stair[-1], 'n', crown[(1, 1)])
bell = max(rooms) + 1
room(bell, 'bell')
link(crown[(1, 0)], 'n', bell)

SPECIAL = {
    hearth: dict(specmon=2129),
    ring: dict(specmon=2128),
    throne: dict(specmon=2127),
    matriarch: dict(specmon=2126),
    bell: dict(cmdtext=10280),
}
# Lairs refill every spawn pass; the bridges and the stair only now and then.
LAIR = {'ledge', 'camp', 'nest', 'eyrie', 'crown'}


def wrap(text, width=70, lines=7):
    out = textwrap.wrap(' '.join(text.split()), width, break_on_hyphens=False)
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
    exits = [f'{DIRS[d]} = {t}' for d, t in
             sorted(r['exits'].items(), key=lambda kv: list(DIRS).index(kv[0]))]
    if n == 1:
        exits.insert(0, f'down = {{ target = {ENTRANCE[1]}, kind = "MapChange", par1 = {ENTRANCE[0]} }}')
    out.append('exits = { ' + ', '.join(exits) + ' }')
    if 'light' in k:
        out.append(f'light = {k["light"]}')
    if 'spawn' in k:
        if rooms[n]['kind'] in LAIR:
            out.append('room_type = "Lair"')
        out += [f'mongroup = {GROUP}', f'minlevel = {k["spawn"][0]}', f'maxlevel = {k["spawn"][1]}',
                f'maxmonsters = {k["max"]}']
    for f, v in SPECIAL.get(n, {}).items():
        out.append(f'{f} = {q(v) if isinstance(v, str) else v}')
    out.append('')

out += ["# The way in: the Pinnacle of Gloomy Mountain gets a way up onto the bridges.",
        '[[room_change]]', f'map = {ENTRANCE[0]}', f'room = {ENTRANCE[1]}',
        'why = "the way up onto the Rocspire"',
        f'set = {{ exits = {{ up = {{ target = 1, kind = "MapChange", par1 = {MAP} }} }} }}',
        'was = { name = "Gloomy Mountain, Pinnacle" }', '']
Path(__file__).resolve().parent.parent.joinpath('rooms.toml').write_text('\n'.join(out))
print(len(order), 'rooms; hearth', hearth, 'ring', ring, 'throne', throne,
      'matriarch', matriarch, 'bell', bell, 'stair', stair[0], '-', stair[-1])
