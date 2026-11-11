# The Rocspire (levels 150–200)

Past the Pinnacle of Gloomy Mountain, a chain of wind-scoured spires where giant rocs nest, and
the white-pelted nomads who hunt them keep a Longhall. This is area 2 of
[`docs/content-areas.md`](../docs/content-areas.md), written as a silvermere content overlay
(silvermere's `docs/overlays.md`). It loads after `mudrev`.

New content for the Realm of Legends. Its nomads, giant roc and hawks are MudRev records that no
room ever used, and so are the crimson battle-shield, titanium shield and sadamune it hands out;
the rest is original.

## Applying it

```
silvermere overlay check rocspire     # safe while the server runs
silvermere overlay apply rocspire     # stop the server first
```

`source/rooms.py` writes `rooms.toml`; run it after changing the layout or a room's text.

## What it adds and changes

| | |
| --- | --- |
| Rooms | 149 new rooms on map 21 |
| Way in | Gloomy Mountain, Pinnacle (3/5661), the starmetal giant king's lair, gets an `up` exit onto the rope bridges |
| Monsters | 3 realm monsters nothing ever spawned, retuned (the blood hawk as a hawk swarm, the nomadic huntsman as a nomad raider, a giant roc); 8 new: frost-pelt shaman, nomad huntmaster, roc broodling, storm elemental, the Roc Matriarch, Jarl Hrafnkel, Ingrid Far-Sworn, Sigrun |
| Items | the pinion and the torc (5125–5126) and the Long Saga's rewards (5127–5134); the unused crimson battle-shield, titanium shield and sadamune drop here |
| Text and messages | Sigrun's talk, the saga and the storm-bell (10260–10282), messages 10350–10370 |

Spawns use monster group 34 (`Group29`), which no realm monster used.

| Zone | Rooms | Spawns |
| --- | --- | --- |
| Rope Bridges | 12 | hawk swarms, nomad raiders (now and then; the wind keeps the light low) |
| Windswept Ledges | 26 | hawk swarms, nomad raiders |
| Nomad Camp | 24 | nomad raiders (crimson battle-shield, titanium shield 1%), frost-pelt shamans (ice spells), nomad huntmasters (the shields 2%) |
| Longhall | 4 | none |
| Saga Hearth | 1 | Sigrun the saga-keeper |
| Champion's Ring | 1 | Ingrid Far-Sworn (9,500 HP; sadamune 25%) |
| Jarl's High Seat | 1 | Jarl Hrafnkel (11,000 HP; his torc, always) |
| Roc Nests and Eyries | 44 | roc broodlings, giant rocs |
| Matriarch's Nest | 1 | the Roc Matriarch (13,000 HP; her pinion, always) |
| Stormcrown Stair | 28 | giant rocs, storm elementals (now and then) |
| Stormcrown | 6 | storm elementals |
| Storm-Bell | 1 | the storm-bell: `ring bell` |

## The quest: The Long Saga

Sigrun keeps the step in ability 212, and whether the storm-bell has rung in 213 (Ashfall Valley
and the Gilded Asylum use 210 and 211).

1. **ask sigrun saga** (level 150+): she names three deeds.
2. In any order: take the Roc Matriarch's pinion, take Jarl Hrafnkel's torc, and **ring bell** at the
   top of the Stormcrown.
3. **ask sigrun deeds** with the pinion and the torc and the bell rung: 500,000,000 experience and,
   by class:
   - **Skald:** a war-harp shield, a saga helm and a runed war-maul (Skalds may only wield blunt
     weapons, so the plan's runed axe is a maul);
   - **Warrior:** a ring-mail hauberk, ring-mail leggings and a bearded greataxe;
   - **Bard:** a saga-singer's jerkin;
   - **Mystic:** storm-wrapped handwraps;
   - anyone else: the experience alone.

The rewards sit a step below each class's best gear in the realm (the Shining and Golden Platemail
and their weapons) and need level 150.

## How it was checked

- `silvermere overlay check` against a copy of the live realm: every exit, monster, item, message
  and text it points at exists.
- **Damage**, by MME's model on the applied copy: the commons do 297–427 a round (band 200–450),
  the bosses 621–705 (band 570–740).
- **Survival**, by the same model against the realm's characters:

  | | Bridges, ledges | Camp | Nests | Stormcrown | Ingrid | Jarl | Matriarch |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | level 77 and below | no | no | 0–50% | no | no | no | no |
  | 102, 116 | yes | yes | yes | yes | no | no | no |
  | 109, 113 | 50% | 33% | 50% | 0–50% | no | no | no |
  | 142 (Skinny) | yes | yes | yes | yes | no | no | no |
  | 143 (Fatty) | yes | yes | yes | yes | yes | yes | no |

  The characters at 142–143 the area is for clear its commons; the Jarl and his champion want the
  strongest of them, and the Roc Matriarch a party.
- **In game**, on a copy of the realm in a test server: the Pinnacle's way up, the bridges, Sigrun's
  greeting and refusals (a missing pinion or torc named, the bell reminded), the storm-bell (once
  for the saga, then only a thud), the Skald's reward, and the ledges' and nests' spawns.

Not on the live realm yet.
