# The Ossuary Court (levels 200–250, and a party raid)

Beneath Lord Magnus's hut in the Dreary Forest, the court of the thing he was bargaining with: a
demon-ruled ossuary of bone and ash, and its master, the Unmaker, who wants the realm's three
alignment relics. This is area 4 of [`docs/content-areas.md`](../docs/content-areas.md), written as
a silvermere content overlay (silvermere's `docs/overlays.md`). It loads after `mudrev` and
`darkwood-quests`, whose 9th alignment quest it continues.

New content for the Realm of Legends. Its bone-knights (the marble knight) and the Death Reaper are
MudRev records that no room ever used; the rest is original. The quest givers and the relics are
Darkwood BBS's.

## Applying it

```
silvermere overlay check ossuary-court     # safe while the server runs
silvermere overlay apply ossuary-court     # stop the server first
```

`source/rooms.py` writes `rooms.toml`; run it after changing the layout or a room's text.

## What it adds and changes

| | |
| --- | --- |
| Rooms | 107 new rooms on map 22 |
| Way in | Dreary Forest, Magnus Hut (2/9811) gets a room command: **go trapdoor** (or **enter trapdoor**) takes a character past step 61 of their alignment's quest (Lord Magnus destroyed) down the bone stair; everyone else finds solid boards. The stair's top room leads back `up` to the hut. |
| Monsters | 2 realm monsters nothing ever spawned: the marble knight retuned as the bone-knight, and the Death Reaper placed as he is, carrying the gate's key; 10 new: ossuary swarm, ash-wraith, chaos demonling, greater hellion, charnel priest, the arachnigoth, Lorzina Herald of Ash, and the Unmaker's three phases |
| Quest givers | Chancellor Annora, The Grey Lord and Balthazar talk from copies of their topic scripts that add **unmaker** (Darkwood's overlay owns the originals) |
| Items | the three relics, upgraded once more (5135–5137), and the ash-black key (5138) |
| Spells | the Unmaker's phase summons and quest step, and the ash-wraith summon (5121–5125) |
| Text and messages | the trapdoor, the 10th quest (10290–10332), messages 10380–10398 |

Spawns use monster group 13 (`Group8`), generation indexes 11–16: no room spawns that group, and its
one realm monster (the horned demon) has index 1.

The chaos demonling, greater hellion, arachnigoth and Lorzina that the plan meant to retune are each
summoned or transformed into somewhere in the realm (by the halfling prisoner, the Champion of Blood,
the Mayor of Arlysia and the beautiful woman), so the court's are new monsters copied from them.

| Zone | Rooms | Spawns |
| --- | --- | --- |
| Bone Stair | 20 | ossuary swarms, bone-knights (now and then, one at a time) |
| Charnel Galleries | 38 | ossuary swarms, bone-knights, ash-wraiths |
| Arachnigoth's Pit | 1 | the arachnigoth (14,000 HP) |
| Herald's Arch | 1 | Lorzina, Herald of Ash (12,500 HP) |
| Court of Ash | 29 | ash-wraiths, chaos demonlings, greater hellions, charnel priests |
| Gate of Bone | 1 | the Death Reaper (21,470 HP; the ash-black key, always) |
| Unmaker's Hall | 16 | greater hellions, charnel priests; behind the locked gate |
| Unmaker's Throne | 1 | the Unmaker |

## The raid: the Unmaker

Three phases, each its own monster, for a party:

1. **Unmaker** (30,000 HP): physical blows.
2. **Unmaker, unveiled** (30,000 HP): armageddon and spheres of annihilation.
3. **Unmaker, unmade** (25,000 HP): physical blows, and raises ash-wraiths from the ash.

Each phase's death spell summons the next; each is worth 800 million experience (under the 32-bit
limit on a kill). The first phase returns 24 hours after the last one dies. The Death Reaper's key
opens the Gate of Bone (`use ash-black east`, then `open east`).

## The quest: the 10th alignment step

Each alignment's quest ability (126 good, 127 neutral, 128 evil) holds the step. Darkwood's 9th quest
ends at 61, when killing Lord Magnus makes the relic whole.

1. **ask annora unmaker** (good), **ask grey unmaker** (neutral) or **ask balthazar unmaker**
   (evil), at step 61: the giver names the Unmaker and sends you down (62).
2. In Magnus's hut, **go trapdoor**, and destroy the Unmaker's last phase. Everyone in the room who
   is on step 61 or 62 of their alignment's quest moves to 63, so a party is counted together.
3. Ask the giver again with the relic (the Aura of Light, Scales of Balance or Icon of Evil): it is
   upgraded, with 3,000,000,000 experience (as the 9th quest gives), and the quest ends at 64.

The upgraded relics keep their names and once-a-day powers; their bonuses rise by half again (the
9th quest doubled the 8th's).

## How it was checked

- `silvermere overlay check` against a copy of the live realm: every exit, monster, item, spell,
  message and text it points at exists, and every `was` matches.
- **Damage**, by MME's model on the applied copy: the commons do 431–544 a round (band 150–600), the
  arachnigoth and Lorzina 774 and 798 (band 620–830), the Death Reaper 1,419, and the Unmaker's
  phases 1,327, 1,350 and 1,418 (party band 1,200–1,800).
- **Survival**, by the same model against the realm's characters, with the four strongest also
  raised to 200, 225 and 250 (gear and stats unchanged):

  | | Stair | Galleries | Court, Hall | Arachnigoth, Lorzina | Reaper, Unmaker |
  | --- | --- | --- | --- | --- | --- |
  | level 77 and below | 0–50% | no | no | no | no |
  | 102–116 | yes | 0–67% | 0–50% | no | no |
  | 142 (Skinny) | yes | 33% | no | no | no |
  | 143 (Fatty) | yes | yes | yes | no | no |
  | 200 (Fatty, Jack) | yes | yes | yes | Fatty | no |
  | 225–250 (the four) | yes | 67–100% | 50–100% | Fatty, Jack | no |

  At 200, two classes (Fatty's Skald and Jack's) clear the commons; the court's champions want the
  strongest of them, and the Death Reaper and the Unmaker a party. Fatty clears the commons already
  at 143, as he did the Rocspire's: his gear is far ahead of anyone else's.
- **In game**, on a copy of the realm in a test server (the Death Reaper and the Unmaker cut to 5 HP
  on that copy only): the trapdoor refusing a character below step 61 and taking one at step 61 down
  (good and neutral) and back up; the Grey Lord's start, reminder, reward and closing lines (his
  Scales upgraded, step 64); the Death Reaper's key unlocking the Gate of Bone; the Unmaker's three
  phases summoning one another, the third raising ash-wraiths and its death moving the killer to
  step 63; the arachnigoth, Lorzina and the zones' spawns. Annora's and Balthazar's lines are the
  Grey Lord's with their own alignment tests; their rooms are behind the realm's own locked doors
  and were not walked.

Not on the live realm yet.
