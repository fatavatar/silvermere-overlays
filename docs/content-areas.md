# New content areas for Realm of Legends

A design proposal for four new areas. It starts from a survey of what the realm has now. Every
number below comes from `rol-server/data/silvermere.db` unless it is marked as a target. Nothing has
been built yet.

## Where the realm stands

### Who plays

There are 15 characters. Twelve of them are level 51 or higher. Six are level 100 or higher (102, 109,
113, 116, 142, 143), and the top character is a level 143 Serpentkin Skald. Only three are level 1.
The Darkwood quests we are bringing in run to level 200.

### What each level band has to hunt

An area's level is the lowest level at which characters of **two different classes** survive at
least 80% of what spawns there. Survival is judged by MajorMUD Explorer's own model (rounds to kill
against rounds to die, solo, using each character's real stats, gear and best attack). How this was
worked out, and how it was checked, is under "How the levels were worked out" below.

| Band | Rooms | Areas | Examples |
| --- | ---: | ---: | --- |
| 1–49 | ~20,900 | ~235 | Stone Tunnel, Blackwood Forest, Volcano, Crystal Lake |
| 50–99 | ~3,200 | ~60 | Darkened Forest (77), Valley of the Undead, Dark Foothills, Rocky Cliffs |
| 100–149 | ~2,100 | ~25 | Dread Forest (102), Ruined Palace (109), Gleaming Caves, Gloomy Mountain (142) |
| 150–199 | ~720 | 13 | Dark Jungle (160), Southwind Dale, Stronghold Basement (180), Granite Castle |
| 200–249 | ~320 | 3 | Earthen Stronghold (200), Petrified Forest, Barren Fields |
| party only | ~6,000 | 45 | Dismagi Cavern, Fields of Kon'fehr, Dreary Forest, Ancestral Cave, Black Quagmire, Ancient Cave |

Solo content thins out steadily as levels rise. That matters because our strongest characters
(142 and 143) are about to step into the two thinnest solo bands, which is also where the Darkwood
quests sit (8th quest from 150, 9th from 200).

The "party only" row means no solo character survives those areas, even raised to level 250 with
today's gear: their lairs hold several monsters that hit for 300–1,800 a round. A few large mixed
areas also land there because one monster type dominates their spawns; Elemental Forest is one, and
the bots solo most of it at 84–92.

Each level above 75 costs a roughly flat 0.2–3 billion experience. (This uses the game's exact
formula, quirks included, and it does not overflow before level 200.) So the high levels are not
short of experience. What they lack is places a solo character can survive.

### Bosses

The realm has about 45 bosses worth roughly 300 million experience or more. The largest are:

- Wicca Overlord (26,999 HP);
- Angel of Bloodshed (26,350 HP);
- Lord Magnus (24,050 HP).

They are spread across Dreary Forest, Ancestral Cave, Dismagi Cavern, Black Quagmire and the
Esoteric Cavern.

### Content built but never used

**70 monsters never appear** (a few are test records). No room spawns them, and no spell or script summons them. Several
form natural sets:

- **Dinosaurs:** Tyrannosaur, deinodon, ankylosaur, stegosaur, triceratops, two tetraraptors,
  pteranodon and deinonychus. All have descriptions; as they stand their stats suit about level 40.
- **Roc hunters:** the nomadic huntsman ("garbed in soft white pelts... several large roc
  feathers"), the giant roc and the blood hawk.
- **Mad magi:**
  - Demented Sorcerer and Deranged Magus (17,100 HP each);
  - a spare Shrefwan the Alchemist (#1385);
  - the trio Choira Pyromancer, Lallim Whitemane and Sharh'Kur;
  - the crazed lunatic and the depraved murderer.
- **Demons and the dead:**
  - Death Reaper (#1371, 21,470 HP);
  - chaos demonling and greater hellion;
  - arachnigoth (a house-sized skeletal spider) and Lorzina;
  - four cloaked figures, the marble knight, the darken beast and the opalescent griffon.

**454 items can't be obtained.** No shop, drop, placement, script or key gives them. Most are junk
(rocks, checks, placeholders), but some is real gear:

- **The Viperhide set:** tunic, leggings, gloves, boots and helm. It is a full mid-level set with
  abilities on every piece.
- **Class gear:**
  - Titanium Chainmail Tunic (Samurai, armour class 40.5 and damage resistance 19.7);
  - golden crossbow (Archer, 60–75 damage);
  - mithril shuriken (Ninja, 45–65);
  - Holy Cross (Templar);
  - Sunburst wrist-guard (Missionary);
  - mirrored choli (Gypsy).
- **Shields and boots:** crimson battle-shield, titanium shield, lunar chainmail boots.
- **Weapons:** sadamune.

### Classes that are short of gear

These are the number of items restricted to each class:

- **Skald: 16.** The highest-level character is a Skald.
- Warrior: 25.
- Mystic: 43.
- Bard: 48.
- Every other class has 51–164.

## Design rules

- **Same record model.** Rooms, monsters, items, spells, scripts and messages work exactly as the
  realm's do. MegaMud and the existing clients see nothing unusual, apart from new map numbers.
- **One new map per area** (maps 19–22, which are unused). Each area joins the world at one
  existing room through a map-change exit (an exit of type Map Change names the destination map),
  so it walks like any other exit; a door or a room command works too where the story wants one.
- **Stats anchored to monsters that already exist.** For each band, these are the realm's monsters
  that first become survivable there, by the same model. New monsters copy their ranges. Damage is
  MME's average damage a round.

  | Band | Common monster | Damage a round | Experience a kill | Boss | Boss damage | Boss experience | Matches |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | 55–80 | 1,200–2,400 HP | 100–200 | 25,000–500,000 | 4,000–9,000 HP | 150–300 | 1–10 million | blue wyvern, frost giant; rakshasha lord |
  | 100–150 | 2,100–4,500 HP | 150–350 | 300,000–550,000 | 6,800–10,500 HP | 280–500 | 45–130 million | young titan, wererat battlemage; dragoon warlords |
  | 150–200 | 2,900–3,600 HP | 200–450 | 300,000–500,000 | 9,500–13,000 HP | 570–740 | 150–280 million | dao shaman, wererat royal guard; wererat king, frosted dragon |
  | 200–250 | 3,500–4,100 HP | 150–600 | 600,000–800,000 | 12,500–14,750 HP | 620–830 | 240–280 million | death mage, dread bishop; Icebane Wizard, sinister mists |
  | party | 4,000–7,000 HP | 300–500 | 0.5–17 million | 15,000–27,000 HP | 1,200–1,800 | 300–790 million | Dismagi; Wicca Overlord, Lord Magnus |

  Every new area is checked against the real characters with the same model before it ships: its
  band's floor should be survivable by two classes, and the band below should not.
- **Two hard limits:**
  - Monster HP is a 16-bit field, so no single monster can have more than 32,767 HP.
  - Experience for a kill is the monster's experience times its level, kept in 32 bits, so it must
    stay under 4.29 billion.
  - Raid bosses therefore come in phases: each phase's death spell summons the next phase, which
    the realm can already do. No engine change is needed.
- **Unused monsters and items are reused before new ones are made.** Nothing refers to them, so
  retuning them breaks nothing.

## Area 1: Ashfall Valley (levels 55–80)

**What it is:** A sunken valley inside the Volcano, kept warm by vents. Lizards that should have
died out still live there, and a serpent cult breeds raptors to guard its temple.

**How you get in:** Volcano, Chiseled Tunnels (16/1900), a dead end whose only exit is northwest.
It gets a `down` exit into the Ashfall Vent (map 19).

**Status: built.** The overlay is `ashfall-valley/` in this repository (see its README): 109 rooms, the
retuned dinosaurs, the Coiled Temple and Tamsin's quest, checked against the survival model and
walked end to end in a test server on a copy of the realm. Not on the live realm yet.

**Size:** about 120 rooms in four parts:

- the vent descent (15 rooms);
- the fern basin (55 rooms; the herbivores roam here);
- the tar pits (25 rooms; the predators hunt here);
- the Coiled Temple (25 rooms; the cult).

**Monsters:**

- The nine unused dinosaurs, raised to the band: 1,200–2,400 HP and 100–200 damage a round.
  Ankylosaur, stegosaur and triceratops are the heavy grazers at the top of that range.
- Raptors (tetraraptor and deinonychus) hunt in packs, as group leader and followers.
- The pteranodon is a roamer.
- The giant locust and scarab swarm are filler.
- **New:** viper cultists and a cult priest (1,500–2,400 HP, using the existing serpent and cultist
  monsters as templates).
- **Bosses:**
  - the Tyrannosaur (raised from 4,750 to about 6,500 HP), alone in the tar pits;
  - the new **Coil Mother**, a giant serpent at the temple's heart (about 9,000 HP), with the
    Viperhide Helm as a guaranteed drop.

**Loot:** the whole Viperhide set, one piece per cult boss or lieutenant (it is unobtainable today).
Raptor claws and tar are sold to an alchemist for coins.

**Quest:** a three-step "break the cult" quest from a ranger at the entrance. It finishes with the
Coil Mother and gives a choice of Viperhide piece.

**Why build it first:**

- Almost every monster already exists, so most of the work is rooms, text, one quest and a stat pass.
- It is the cheapest way to prove the overlay loader on a whole new map.
- It serves the characters at 54, 69 and 76–77, and any alts.

## Area 2: The Rocspire (levels 150–200)

**What it is:** Past the Pinnacle of Gloomy Mountain, a chain of wind-scoured spires where giant
rocs nest. The white-pelted nomads who hunt them keep a longhall there. It is the next step for the
characters now at 142–143, whose solo choices run out at Dark Jungle and Stronghold Basement.

**How you get in:** Gloomy Mountain, Pinnacle (3/5661), the starmetal giant king's lair, whose only
exit is down. A new `up` exit leads onto a rope bridge (map 20). Gloomy Mountain itself
rates 142, and characters on the Darkwood 8th quest (level 150) already climb here, so the starmetal
giant king guards both paths.

**Size:** about 150 rooms:

- the rope bridges and ledges (40 rooms; wind keeps light low);
- the roc nests (45);
- the nomad camp and Longhall (30);
- the Stormcrown (35), the highest spire.

**Monsters:**

- **Retuned to the band:** the nomadic huntsman becomes nomad raiders and huntmasters (2,900–3,600
  HP, 200–450 damage a round); the giant roc becomes a roaming roc at the top of that range; the
  blood hawk becomes a hawk swarm.
- **New:**
  - frost-pelt shamans (spellcasters, using the realm's ice spells);
  - storm elementals around the Stormcrown;
  - roc broodlings (low HP, high damage, in groups).
- **Bosses:**
  - **the Roc Matriarch**, about 13,000 HP and 700 damage a round, in the highest nest;
  - **Jarl Hrafnkel**, the nomad chief in the Longhall, about 11,000 HP.

**The Long Saga.** This is a class quest at the Longhall for the classes that are shortest of gear:

- **Who:** Skalds and Warriors. Bards and Mystics get a shorter branch.
- **How it works:**
  - A blind saga-keeper NPC asks for deeds: a roc feather from the Matriarch, the Jarl's torc, and
    ringing the storm-bell at the top of the Stormcrown (a room command there records the step).
  - Each deed is worth a verse.
- **The reward:** new gear made for those classes.
  - **Skald:** a war-harp shield, a saga helm, a runed axe. These are the first Skald gear in the
    realm worth chasing at this level, and the realm's top character is a level 143 Skald.
  - **Warrior:** a set of ring-mail and a greataxe.
  - **Bards and Mystics:** one item each.

**Loot:** the unused crimson battle-shield and titanium shield drop from the raiders. The sadamune
goes to the Jarl's champion.

## Area 3: The Gilded Asylum (levels 100–150)

**Status: built.** The overlay is `gilded-asylum/` in this repository (see its README): 75 rooms on
map 20, the retuned patients and laboratory bosses, the three ward heads, Ines's quest and her
potions, checked against the survival model and walked end to end in a test server on a copy of
the realm. Not on the live realm yet. It differs from the plan below in three places:

- The ward heads (Choira Pyromancer, Lallim Whitemane, Sharh'Kur) and the cloaked figures are
  still used by the realm's own quests and rooms, so the asylum's are new monsters copied from
  them rather than retunes. Only the crazed lunatic and depraved murderer it retunes, and
  Shrefwan, the Sorcerer and the Magus, were unused.
- A text exit (`climb panel`) cannot change maps, so the panel leads to a new crawlspace room on
  map 9 (9/1500), which climbs up to the asylum. There is no `search` step.
- It has 75 rooms rather than about 90: three wards of 18–22 rooms, the corridors, the dispensary
  and the laboratory.

**What it is:** The madhouse above the Padded Cells (map 9) has sealed upper wards. Patients were
"treated" there with alchemy until the alchemist Shrefwan began treating himself. The furniture is
gilded, and everything else is wrong.

**How you get in:** Padded Cell (9/1255), whose only exit is north. A loose ceiling panel ("search"
finds it, then "climb panel") leads up. The lower Padded Cells (levels 1–9) stay as they are, a joke
the realm has already set up.

**Size:** about 90 rooms over three wards and a laboratory:

- the Ward of Whispers (illusion monsters);
- the Ward of Fevers (fire);
- the Ward of Chains (the violent wards);
- Shrefwan's laboratory.

**Monsters:**

- **Retuned:**
  - the crazed lunatic and depraved murderer become "treated" patients (2,100–4,500 HP);
  - the four cloaked figures become wardens.
- **New:**
  - orderlies;
  - animated straitjackets (they cast Hold Person);
  - mirror-patients that summon copies of themselves.
- **Ward bosses**, each holding one reagent:
  - Choira Pyromancer (Ward of Fevers);
  - Lallim Whitemane (Ward of Whispers);
  - Sharh'Kur (Ward of Chains).
  - All three are retuned from 380–475 HP to about 8,000–10,000.
- **Final pair:** the Demented Sorcerer and the Deranged Magus (cut from 17,100 to about 10,000 HP
  each) guard the laboratory door. Each
  one's death spell summons two orderlies, so the fight gets busier, not easier.
- **Final boss:** **Shrefwan the Alchemist** (the spare #1385) at about 10,500 HP. When he falls he gulps
  a potion and rises as a second form: his death spell summons it, the same way the Unmaker's phases
  work.

**Loot:** the unused class gear finally goes somewhere:

- Titanium Chainmail Tunic (Samurai);
- golden crossbow (Archer);
- mithril shuriken (Ninja);
- Holy Cross (Templar);
- Sunburst wrist-guard (Missionary);
- mirrored choli (Gypsy).

Each comes from a ward boss or from Shrefwan's cabinet. A surviving apothecary in the wards trades
the three reagents (a script NPC) for one-use potions with long-lasting effects.

## Area 4: The Ossuary Court (levels 200–250, and a party raid)

**What it is:**

- When Lord Magnus dies (the end of the Darkwood 9th quest), a trapdoor under his hut stops being
  hidden.
- Below it lies the court of the thing Magnus was bargaining with: a demon-ruled ossuary.
- Its master, **the Unmaker**, wants the realm's three alignment relics (the Aura of Light, the
  Scales of Balance and the Icon of Evil).

**How you get in:** Dreary Forest, Magnus Hut (2/9811), whose only exit is southeast. A room
command there ("open trapdoor" / "go trapdoor") moves only characters past quest step 61. Its
script checks the quest step, as the Darkwood castle filter does.

**Size:** about 110 rooms:

- the bone stair (20);
- the Charnel Galleries (40);
- the Court of Ash (30);
- the Unmaker's throne (20).

**Monsters:**

- **Retuned:**
  - the chaos demonling and greater hellion (about 4,000 HP and 600,000–800,000 experience; they
    are 4,750 and 5,510 today);
  - the arachnigoth (about 14,000 HP) as a lair boss;
  - Lorzina as the court's herald.
- **New:**
  - bone-knights (with the marble knight as their template);
  - ossuary swarms;
  - ash-wraiths.
- **Champion:** the Death Reaper (#1371, already 21,470 HP and 462 million experience) guards the
  Court of Ash. Like the realm's other bosses of that size, he is party content.
- **Raid boss (a party fight): the Unmaker, in three phases:**
  - phase 1: 30,000 HP, physical attacks;
  - phase 2: 30,000 HP, casts the realm's strongest area spells;
  - phase 3: 25,000 HP, summons ash-wraiths.
  - Each phase's death spell summons the next. Each phase is worth about 800 million experience,
    which stays under the 32-bit kill limit.

**Quest: the 10th alignment step.**

- **Steps:** a short epilogue for each alignment's quest (steps 61→64). Each step's giver sends you
  into the court, and killing the Unmaker's third phase completes the quest.
- **Reward:** the alignment relic is upgraded once more, as Darkwood's 9th quest does.
- **It is optional:** without the Darkwood quests, this area still works as plain endgame hunting.

## How the levels were worked out

- **The survival model.** mudtool is the browser port of MajorMUD Explorer (by Syntax), and it
  reads our own `mudrev.mdb`. A small harness (`tools/area-survival/`) built our 11 fighting
  characters (levels 54–143; the level 51 healer bot was left out) in it, using their real class,
  race, stats, worn gear, weapon and spellbook. It then asked MME's exp/hour pipeline about every
  monster the realm spawns. That pipeline returns "not killable" when the character would die before
  the monster (MME's `IsMobKillable`: rounds to kill against rounds to die, including both sides'
  regeneration). Each character fought with whichever of its weapon or damage spells kills the most.
- **Beyond level 143**, the four strongest characters were raised to 160, 180, 200, 225 and 250
  with their gear and stats unchanged.
- **The checks:**
  - **The bots' hunting history** in mudstats (which path each looped, at which levels, for how
    many laps). The bots farm the Ancient Galleon at 43–55, Ruined Palace at 87–117 and Stronghold
    Basement at 120–143. The model agrees: the level 54 character survives the Galleon, Ruined
    Palace rates 109, and the level 143 character is the first to survive Stronghold Basement.
  - **The alignment quests' level gates.** Dark Jungle (8th quest, 150) rates 160.
  - **Your note:** Gloomy Mountain is 150+, and it rates 142.
- **Where it is rough:**
  - It is a solo model with no buffs and no healing, so it is cautious.
  - Twelve characters leave gaps (nobody between 77 and 102, or between 116 and 142), so band
    edges can be 10–20 levels off.
  - Below level 54 the older experience-based estimate is kept.

## What it takes to build

| | Rooms | New monsters | Retuned | New items | Reused items | Quest steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ashfall Valley | ~120 | 3 | 13 | ~4 | 5 | 3 |
| The Rocspire | ~150 | 6 | 3 | ~8 | 3 | ~6 |
| The Gilded Asylum | ~90 | 4 | 10 | ~6 | 6 | ~5 |
| The Ossuary Court | ~110 | 6 | 6 | ~4 | 0 | 3 per alignment |

**Engine work:**

- **Content overlay loader:** the only real piece. It loads new maps and records, and set/was
  changes to existing ones, on top of the imported realm. The Darkwood quests need it too, so it
  gets built once for both.
- **Everything else** uses mechanics the realm already has: death spells, summons, room command
  scripts, quest abilities and lair generation.

**Order:**

1. Ashfall Valley, which proves the loader.
2. The Rocspire, which serves the top characters as they reach 150.
3. The Ossuary Court, which pairs with the Darkwood quests.
4. The Gilded Asylum.

## Open questions

1. **The classes for the Long Saga.** Skald and Warrior are the clear cases. Do you want Bard and
   Mystic in it too?
2. **The Ossuary Court and the alignment items.** Should it upgrade them again (a 10th quest), or
   stay a plain hunting area?
3. **Names and tone.** Ashfall, Rocspire, Gilded Asylum and Ossuary Court are placeholders. The
   Asylum is played half for laughs, as the Padded Cells already are; say if you want it grim
   instead.
4. **Reusing unused monsters in place versus copying them to new numbers.** In place is simpler, and
   nothing refers to them today.
