# The Gilded Asylum (levels 100–150)

The madhouse above the Padded Cells has sealed upper wards. The alchemist Shrefwan "cured" its
patients with gold until he cured himself; now everything is gilded and everything is wrong. This
is area 3 of [`docs/content-areas.md`](../docs/content-areas.md), written as a silvermere content
overlay (silvermere's `docs/overlays.md`). It loads after `mudrev`.

New content for the Realm of Legends. Shrefwan, the Demented Sorcerer and the Deranged Magus, and
the six pieces of class gear it hands out, are MudRev records that nothing ever placed; the rest
is original.

## Applying it

```
silvermere overlay check gilded-asylum     # safe while the server runs
silvermere overlay apply gilded-asylum     # stop the server first
```

`source/rooms.py` writes `rooms.toml`; run it after changing the layout or a room's text.

## What it adds and changes

| | |
| --- | --- |
| Rooms | 75 new rooms on map 20, and the Padded Cell's crawlspace (9/1500) |
| Way in | Padded Cell (9/1255) gets a loose ceiling panel: `climb panel` (a text exit), then `up` |
| Monsters | 5 realm monsters nothing ever spawned, retuned (the crazed lunatic and depraved murderer as "treated" patients, Shrefwan, the Sorcerer, the Magus); 10 new: mirror-patient, mirror image, orderly, animated straitjacket, warden, the three ward heads, Shrefwan transfigured, Ines |
| Items | the three reagents, the gilded key and three potions (5110–5116); the unused class gear drops in the asylum |
| Spells | 5110–5120: the summons, the quest kill, the potions |
| Text and messages | Ines's talk and quest (10230–10255), messages 10320–10347 |

Spawns use monster group 33 (`Group28`), which no realm monster used, so the asylum's rooms draw
only its own monsters. Every ward room is a lair.

| Zone | Rooms | Spawns |
| --- | --- | --- |
| Attic Landing, Gilded Corridor, Rotunda | 5 | none |
| Dispensary | 1 | Ines the apothecary |
| Ward of Whispers | 18 | treated lunatics, mirror-patients (they split off mirror images), orderlies |
| Whispering Gallery | 1 | Lallim Whitemane (8,000 HP): quicksilver tears, mirrored choli 25% |
| Ward of Fevers | 18 | orderlies, treated murderers |
| Furnace Room | 1 | Choira Pyromancer (8,500 HP): ember salts, Sunburst wrist-guard 25% |
| Ward of Chains | 22 | treated murderers, animated straitjackets (they cast Hold Person), wardens |
| Iron Cell | 1 | Sharh'Kur (9,500 HP): iron filings, Titanium Chainmail Tunic 25% |
| Laboratory Stair | 2 | none |
| Sorcerer's and Magus's Landings | 2 | the Demented Sorcerer and the Deranged Magus (10,000 HP each; golden crossbow and mithril shuriken 30%). Each one's death brings two orderlies running. |
| Laboratory, Alchemical Sanctum | 3 | Shrefwan (10,500 HP), behind doors locked with the gilded key (`use gilded key south`, then `open south`). His death summons Shrefwan transfigured (9,800 HP; Holy Cross 35%). |

Shrefwan's two forms need a weapon of magic level 3 to hit, the wardens one of level 2 (the realm
records they copy wanted 5 and 4).

## The quest: The Gilded Cure

Ines, in the dispensary, keeps the step in ability 211 (Ashfall Valley's quest uses 210).

1. **ask ines shrefwan** (level 100+): she asks for one reagent from each ward head.
2. **ask ines reagents** with all three: she casts the gilded key (150,000,000 experience).
3. Kill Shrefwan, then Shrefwan transfigured.
4. **ask ines shrefwan**: a draught of iron, of embers and of clarity, and 350,000,000 experience.

From step 2 on, **ask ines ember**, **quicksilver** or **iron** with that reagent trades it for a
potion: embers (+5 damage, faster healing), clarity (+25 magic resistance, +10 spellcasting, +5
intellect) or iron (+10 armour class, +5 damage resistance). Each lasts 1,200 rounds.

## How it was checked

- `silvermere overlay check` against a copy of the live realm (with MudRev, Ashfall Valley and
  Darkwood applied): every exit, monster, item, spell, message and text it points at exists.
- **Damage**, by MME's model (silvermere's MME export on the applied copy): the wards' monsters
  do 190–360 a round, the bosses 310–470, inside the band's 150–350 and 280–500.
- **Survival**, by the same model (`tools/area-survival/zone.mjs`) against the realm's
  characters:

  | | Whispers | Fevers | Chains | ward heads | Sorcerer, Magus | Shrefwan (both) |
  | --- | --- | --- | --- | --- | --- | --- |
  | level 69 and below | no | no | no | no | no | no |
  | 76–77 | 67–100% | 0–50% | 0–33% | no | no | no |
  | 102 (Damyr) | yes | yes | yes | yes | yes | yes |
  | 109, 113 | yes | 50–100% | 33–67% | Lallim only | no | no |
  | 116, 142, 143 | yes | yes | yes | yes | yes | yes |

  The floor of the band clears the wards; the bosses want the band's stronger characters or a
  party, as the realm's own bosses of this size do. The 76–77 characters can manage the Ward of
  Whispers, the one by the entrance, and little else.
- **In game**, on a copy of the realm in a test server: the panel, the crawlspace and the rooms;
  Ines's greeting, topics and refusals; the reagents for the key; the key door; the Sorcerer's
  death bringing two orderlies; Shrefwan's death raising his second form; the second form's
  death moving the quest on and dropping the Holy Cross; Ines's reward and her potion trade; a
  potion's effect; and the wards' spawns.

Not on the live realm yet.
