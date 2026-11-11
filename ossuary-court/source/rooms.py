"""Writes ../rooms.toml: the Ossuary Court's rooms on map 22 and the trapdoor under Lord Magnus's
hut.

The layout is drawn here as grids and chains so the exits always pair up; the room kinds
(name, description, spawns) are in KINDS. Run it after changing either:

    python3 source/rooms.py
"""
import textwrap
from pathlib import Path

MAP = 22
ENTRANCE = (2, 9811)      # Dreary Forest, Magnus Hut: Lord Magnus's lair, only exit southeast
GROUP = 13                # monster group 13 (Group8): no room spawns it; its one monster is index 1
TRAPDOOR = 10290          # the hut's room command (text.toml)
KEY = 5138                # the ash-black key, from the Death Reaper (items.toml)
DIRS = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west', 'u': 'up', 'd': 'down',
        'ne': 'northeast', 'nw': 'northwest', 'se': 'southeast', 'sw': 'southwest'}
BACK = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u',
        'ne': 'sw', 'sw': 'ne', 'nw': 'se', 'se': 'nw'}

# Generation index by spawn tier (monsters.toml): 11 ossuary swarm, 12 bone-knight, 13 ash-wraith,
# 14 chaos demonling, 15 greater hellion, 16 charnel priest.
KINDS = {
    'stair': dict(
        name='Ossuary Court, Bone Stair',
        desc="""A stair winds down into the dark, and every step of it is made of bone: thigh
        bones laid side by side and bound with black wire, skulls set into the walls as
        lamps that do not burn. The air grows warmer as you go down, and it smells of
        dust and old smoke.""",
        spawn=(11, 12), max=1, light=-50),
    'gallery': dict(
        name='Ossuary Court, Charnel Galleries',
        desc="""Galleries of bone run off into the dark in every direction, their walls stacked
        to the ceiling with skulls in neat rows, all of them turned to watch the middle of
        the passage. Some of the rows are new. Somewhere ahead, bones clatter as something
        sorts through them.""",
        spawn=(11, 13), max=2, light=-50),
    'pit': dict(
        name="Ossuary Court, Arachnigoth's Pit",
        desc="""The gallery floor gives way to a pit lined with webs as thick as ship's rope,
        hung with bundled shapes that were once people. At the bottom, something the size
        of a house unfolds its legs one at a time. It is made entirely of bone, and it is
        very, very hungry."""),
    'arch': dict(
        name="Ossuary Court, the Herald's Arch",
        desc="""A high arch of fused skulls opens onto a red glow beyond. Before it stands a
        tall, beautiful woman in a gown of grey ash, a staff of black bone in her hand. She
        smiles as you approach. "You are expected," she says. "The Court will see you
        now. Most of you.\""""),
    'court': dict(
        name='Ossuary Court, Court of Ash',
        desc="""A vast hall opens under a ceiling lost in smoke. Ash falls here like snow, ankle
        deep and still warm, and pillars of bone rise out of it to hold up the dark.
        Demons cross the court on errands of their own, and the dead kneel in rows along
        the walls, waiting to be judged.""",
        spawn=(13, 16), max=2),
    'gate': dict(
        name='Ossuary Court, Gate of Bone',
        desc="""The court ends at a great gate of black bone, bolted shut and carved with a
        single eye. Before it stands a figure twelve feet tall in a hooded cloak of shadow,
        a scythe resting on its shoulder. It does not move, but the ash around its feet
        has stopped falling."""),
    'hall': dict(
        name="Ossuary Court, the Unmaker's Hall",
        desc="""A long hall of bone runs on beyond the gate. Its walls are built from the
        skeletons of things that were never men: wings, horns, coiled spines, a skull with
        three eye sockets. Every one of them has been carefully taken apart and put back
        together wrong.""",
        spawn=(15, 16), max=2),
    'throne': dict(
        name="Ossuary Court, the Unmaker's Throne",
        desc="""At the end of the hall a throne of bone rises out of a lake of ash, and on it
        sits something that has been taken apart and put back together many times, each
        time larger. Three empty niches in the throne's back wait for a halo, a pair of
        scales and an icon. It turns its head towards you, and the whole court goes
        quiet."""),
}

rooms = {}        # number -> dict(kind, exits {dir: target})
order = []


def room(n, kind):
    rooms[n] = dict(kind=kind, exits={})
    order.append(n)


def link(a, d, b, door=False):
    assert d not in rooms[a]['exits'], (a, d)
    assert BACK[d] not in rooms[b]['exits'], (b, BACK[d])
    rooms[a]['exits'][d] = (b, door)
    rooms[b]['exits'][BACK[d]] = (a, door)


def grid(first, w, h, kind_at, holes=()):
    """Rooms numbered row by row from `first`; returns {(x, y): number}."""
    cells, n = {}, first
    for y in range(h):
        for x in range(w):
            if (x, y) in holes:
                continue
            cells[(x, y)] = n
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


# the bone stair: 20 rooms winding down from the trapdoor
stair = chain(1, 'stair', ['d', 's', 'd', 'w', 'd', 's', 'd', 'e', 'd', 's',
                           'd', 'e', 'd', 'n', 'd', 'e', 'd', 's', 'd'])

# the Charnel Galleries, 8 x 5, and the arachnigoth's pit below their far corner
nxt = max(rooms) + 1
galleries = grid(nxt, 8, 5, lambda x, y: 'gallery', holes={(2, 1), (5, 3)})
link(stair[-1], 's', galleries[(3, 0)])
pit = max(rooms) + 1
room(pit, 'pit')
link(galleries[(7, 4)], 'd', pit)

# the Herald's Arch, then the Court of Ash, 6 x 5, and the Gate of Bone at its far side
arch = max(rooms) + 1
room(arch, 'arch')
link(galleries[(7, 2)], 'e', arch)
nxt = max(rooms) + 1
court = grid(nxt, 6, 5, lambda x, y: 'court', holes={(2, 2)})
link(arch, 'e', court[(0, 2)])
gate = max(rooms) + 1
room(gate, 'gate')
link(court[(5, 2)], 'e', gate)

# behind the locked gate, the Unmaker's Hall and his throne
hall = chain(max(rooms) + 1, 'hall', ['e', 'e', 'n', 'e', 'e', 'n', 'n', 'e', 'e', 's',
                                      'e', 'e', 's', 's', 'e'])
link(gate, 'e', hall[0], door=True)
throne = max(rooms) + 1
room(throne, 'throne')
link(hall[-1], 'e', throne)

SPECIAL = {
    pit: dict(specmon=2135),
    arch: dict(specmon=2136),
    gate: dict(specmon=1371),
    throne: dict(specmon=2137),
}
# Lairs refill every spawn pass; the stair only now and then.
LAIR = {'gallery', 'court', 'hall'}


def wrap(text, width=70, lines=7):
    out = textwrap.wrap(' '.join(text.split()), width, break_on_hyphens=False)
    assert len(out) <= lines, (text[:40], len(out))
    return out


def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def exit_toml(d, target, door):
    if door:
        return (f'{DIRS[d]} = {{ target = {target}, kind = "Key", par1 = {KEY}, par2 = 2, '
                f'par3 = -999, par4 = 1 }}')
    return f'{DIRS[d]} = {target}'


out = ['# Generated by source/rooms.py; edit that and run it again.', '',
       '[defaults.room]', 'regendelay = 5', '']
for n in order:
    r, k = rooms[n], KINDS[rooms[n]['kind']]
    out += ['[[room]]', f'map = {MAP}', f'room = {n}', f'name = {q(k["name"])}',
            'desc = """\n' + '\n'.join(wrap(k['desc'])) + '\n"""']
    exits = [exit_toml(d, t, door) for d, (t, door) in
             sorted(r['exits'].items(), key=lambda kv: list(DIRS).index(kv[0]))]
    if n == 1:
        exits.insert(0, f'up = {{ target = {ENTRANCE[1]}, kind = "MapChange", par1 = {ENTRANCE[0]} }}')
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

out += ["# The way in: Lord Magnus's hut gets a trapdoor, which opens only for those who destroyed him",
        "# (step 61 of their alignment's quest; text.toml).",
        '[[room_change]]', f'map = {ENTRANCE[0]}', f'room = {ENTRANCE[1]}',
        'why = "the trapdoor down to the Ossuary Court"',
        f'set = {{ cmdtext = {TRAPDOOR} }}',
        'was = { name = "Dreary Forest, Magnus Hut", cmdtext = 0 }', '']
Path(__file__).resolve().parent.parent.joinpath('rooms.toml').write_text('\n'.join(out))
print(len(order), 'rooms; pit', pit, 'arch', arch, 'gate', gate, 'hall', hall[0], '-', hall[-1],
      'throne', throne, 'stair bottom', stair[-1])
