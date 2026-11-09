"""Writes ../rooms.toml: Ashfall Valley's rooms on map 19 and the way in from the Volcano.

The layout is drawn here as grids and chains so the exits always pair up; the room kinds
(name, description, spawns) are in KINDS. Run it after changing either:

    python3 source/rooms.py
"""
import textwrap
from pathlib import Path

MAP = 19
ENTRANCE = (16, 1900)          # Volcano, Chiseled Tunnels: a dead end
DIRS = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west', 'u': 'up', 'd': 'down',
        'ne': 'northeast', 'nw': 'northwest', 'se': 'southeast', 'sw': 'southwest'}
BACK = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u',
        'ne': 'sw', 'sw': 'ne', 'nw': 'se', 'se': 'nw'}

# Monster group 18 (Group13) holds only Ashfall's monsters. Generation index by spawn tier:
# 1 grazers, 2 raptors, 3 pteranodon, 4 giant locust, 5 deinodon, 6 scarab swarm,
# 7 viper cultist, 8 cult priest.
KINDS = {
    'vent': dict(
        name='Ashfall Vent',
        desc="""A narrow fissure drops away from the volcano's tunnels, its walls glazed
        black where lava once ran. Warm, wet air rises past you, heavy with sulphur and,
        strangely, with the smell of growing things. Handholds have been cut into the
        rock and worn smooth by many hands, and by some things that were not hands."""),
    'mouth': dict(
        name='Ashfall Vent, Mouth',
        desc="""The fissure opens onto a ledge above a wide green valley. Far below, mist
        drifts over a sea of giant ferns, and the volcano's walls rise on every side to a
        roof of rock lit red by distant fires. Something huge bellows in the haze, and a
        flock of leathery shapes wheels away from the sound."""),
    'basin': dict(
        name='Ashfall Valley, Fern Basin',
        desc="""Ferns taller than a man crowd around you, their fronds beaded with warm
        water. The ground is soft black ash that takes every footprint, and many of the
        prints here are larger than your hand and end in long claws. Steam hisses from
        cracks in the earth, and the air is thick enough to drink.""",
        spawn=(1, 3), max=2),
    'pool': dict(
        name='Ashfall Valley, Steaming Pool',
        desc="""A pool of milky water bubbles gently in a hollow among the ferns, ringed
        with trampled mud. Great beasts come here to drink, and the bank is churned into
        deep ruts by their weight. A sour, mineral smell rises with the steam.""",
        spawn=(1, 3), max=2),
    'camp': dict(
        name="Ashfall Valley, Ranger's Camp",
        desc="""A ring of sharpened stakes guards a small clearing on a rise above the
        ferns. A lean-to of hides stands against the rock, and a fire burns low under a
        rack of drying meat. Bones of enormous size have been stacked carefully by the
        stakes, as if someone has been counting."""),
    'tent': dict(
        name="Ashfall Valley, Trading Tent",
        desc="""Under a patched canvas awning, crates and sacks have been stacked against
        the rock: coils of rope, lamp oil, bundles of arrows and a barrel of salt meat. A
        slate hung from the pole reads, in a careful hand, TAKE WHAT YOU NEED. BRING BACK
        WHAT YOU CAN."""),
    'tar': dict(
        name='Ashfall Valley, Tar Pits',
        desc="""The ferns give way to a stinking flat of black pools that bubble and
        steam. A narrow crust of dried tar winds between them, and the ribs of some great
        beast jut from the nearest pit where it sank long ago. Every step sticks, and
        every sound carries.""",
        spawn=(2, 5), max=3),
    'bones': dict(
        name='Ashfall Valley, Bone Field',
        desc="""Bones lie everywhere here, bleached and cracked, some longer than you are
        tall. Most of them have been gnawed. A few still carry scraps of hide, and the
        flies are thick and patient.""",
        spawn=(2, 5), max=3),
    'hollow': dict(
        name='Ashfall Valley, Tar Pit Hollow',
        desc="""The tar flats sink into a broad hollow ringed with trampled ferns and the
        wreckage of things too slow to escape. The ground shakes with a slow, heavy
        rhythm, and a stench of rotting meat hangs in the hot air. This is the lair of
        whatever rules the valley."""),
    'court': dict(
        name='Coiled Temple, Outer Court',
        desc="""Black basalt pillars carved as rearing serpents ring a courtyard of
        cracked flagstones. Scale-patterned banners hang limp in the heat, and offerings
        of meat rot on low stone altars. The temple beyond is half buried in the valley
        wall, its doorway a serpent's open mouth.""",
        spawn=(6, 7), max=2),
    'hall': dict(
        name='Coiled Temple, Serpent Hall',
        desc="""A long hall winds into the rock in slow coils, its walls carved with a
        single endless snake. Braziers burn with a greenish flame, and the floor is worn
        into a shallow channel down the middle, as if something long and heavy has slid
        along it for centuries.""",
        spawn=(7, 8), max=2),
    'pens': dict(
        name='Coiled Temple, Brood Pens',
        desc="""Iron grates close off pits cut into the floor, and from below comes a
        chorus of hissing and the scrape of claws. Cultists have scratched tallies on the
        walls beside each pit. Straw, blood and broken eggshell are trodden into the
        stone.""",
        spawn=(2, 7), max=3),
    'ante': dict(
        name='Coiled Temple, Antechamber',
        desc="""The hall ends at a pair of tall doors of black stone, bound in iron and
        carved with two serpents whose bodies twine into a lock. Something breathes on
        the other side, slowly, with a sound like wind in a cave.""",
        spawn=(7, 8), max=2),
    'sanctum': dict(
        name='Coiled Temple, Sanctum',
        desc="""A vast round chamber opens beneath a dome of raw rock. Coils of scaled
        flesh as thick as a tree trunk fill half the floor, rising and falling with each
        breath, and eggs the size of barrels lie in a nest of bones. Two pale eyes open
        in the dark above you."""),
}

rooms = {}        # number -> dict(kind, exits {dir: target or dict})
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


# the vent: a chain of 12 rooms winding down
path = ['d', 'd', 'n', 'd', 'e', 'd', 's', 'd', 'e', 'd', 'n']
for i in range(1, 13):
    room(i, 'mouth' if i == 12 else 'vent')
for i, d in enumerate(path, start=1):
    link(i, d, i + 1)

# the fern basin, 10 x 5 with a few holes; pools scattered through it
pools = {(2, 1), (6, 3), (8, 0)}
basin = grid(13, 10, 5, lambda x, y: 'pool' if (x, y) in pools else 'basin',
             holes={(3, 3), (4, 0), (7, 2), (9, 4)})
link(12, 'n', basin[(0, 4)])

# the ranger's camp west of the basin, and the trading tent beside it
nxt = max(rooms) + 1
room(nxt, 'camp'); room(nxt + 1, 'camp'); room(nxt + 2, 'tent')
link(basin[(0, 2)], 'w', nxt)
link(nxt, 'n', nxt + 1)
link(nxt, 'w', nxt + 2)
camp, tent = nxt, nxt + 2

# the tar pits east of the basin, 5 x 5, bone fields on the edges; the hollow beyond
nxt = max(rooms) + 1
tar = grid(nxt, 5, 5, lambda x, y: 'bones' if x in (0, 4) and y in (0, 4) else 'tar',
           holes={(2, 2)})
link(basin[(9, 2)], 'e', tar[(0, 2)])
hollow = max(rooms) + 1
room(hollow, 'hollow')
link(tar[(4, 2)], 'e', hollow)

# the Coiled Temple north of the basin: court 3 x 3, the hall, the pens, the sanctum
nxt = max(rooms) + 1
court = grid(nxt, 3, 3, lambda x, y: 'court')
link(basin[(5, 0)], 'n', court[(1, 2)])
hall = list(range(max(rooms) + 1, max(rooms) + 7))
for n in hall:
    room(n, 'hall')
link(court[(1, 0)], 'n', hall[0])
for a, b, d in zip(hall, hall[1:], ['n', 'ne', 'n', 'nw', 'n']):
    link(a, d, b)
nxt = max(rooms) + 1
pens = grid(nxt, 2, 3, lambda x, y: 'pens')
link(hall[2], 'e', pens[(0, 1)])
ante = max(rooms) + 1
room(ante, 'ante')
link(hall[-1], 'n', ante)
sanctum = ante + 1
room(sanctum, 'sanctum')
link(ante, 'n', sanctum)

SPECIAL = {
    camp: dict(specmon=2103),
    hollow: dict(specmon=508),
    sanctum: dict(specmon=2102),
}
# Lairs refill to their maximum every spawn pass; the other spawning rooms only get a monster
# now and then while someone stands in them. The open valley is half lairs (the pools and every
# other room, like a checkerboard), the temple all lairs.
ALWAYS_LAIR = {'pool', 'court', 'hall', 'pens', 'ante'}
CHECKER_LAIR = {'basin', 'tar', 'bones'}


def is_lair(n):
    kind = rooms[n]['kind']
    if kind in ALWAYS_LAIR:
        return True
    return kind in CHECKER_LAIR and sum(coords.get(n, (0, 1))) % 2 == 0


# the sanctum doors: locked, opened by the obsidian serpent key, not pickable
DOOR = dict(kind='Key', par1=5102, par2=2, par3=-999, par4=1)


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
        if {n, t} == {ante, sanctum}:
            exits.append(f'{DIRS[d]} = {{ target = {t}, kind = "Key", par1 = {DOOR["par1"]}, '
                         f'par2 = {DOOR["par2"]}, par3 = {DOOR["par3"]}, par4 = {DOOR["par4"]} }}')
        else:
            exits.append(f'{DIRS[d]} = {t}')
    if n == 1:
        exits.insert(0, f'up = {{ target = {ENTRANCE[1]}, kind = "MapChange", par1 = {ENTRANCE[0]} }}')
    out.append('exits = { ' + ', '.join(exits) + ' }')
    if 'spawn' in k:
        if is_lair(n):
            out.append('room_type = "Lair"')
        out += ['mongroup = 18', f'minlevel = {k["spawn"][0]}', f'maxlevel = {k["spawn"][1]}',
                f'maxmonsters = {k["max"]}']
    for f, v in SPECIAL.get(n, {}).items():
        out.append(f'{f} = {q(v) if isinstance(v, str) else v}')
    out.append('')

out += ['# The way in: the dead end of the Volcano\'s chiseled tunnels gets a way down.',
        '[[room_change]]', f'map = {ENTRANCE[0]}', f'room = {ENTRANCE[1]}',
        'why = "the way down into Ashfall Valley"',
        f'set = {{ exits = {{ down = {{ target = 1, kind = "MapChange", par1 = {MAP} }} }} }}',
        'was = { name = "Volcano, Chiseled Tunnels" }', '']
Path(__file__).resolve().parent.parent.joinpath('rooms.toml').write_text('\n'.join(out))
print(len(order), 'rooms,', sum(1 for n in order if 'spawn' in KINDS[rooms[n]['kind']] and is_lair(n)), 'lairs; camp', camp, 'tent', tent, 'hollow', hollow, 'ante', ante, 'sanctum', sanctum)
