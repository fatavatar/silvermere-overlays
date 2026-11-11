# silvermere overlays

Content overlays for [silvermere](https://github.com/fatavatar/silvermere), the MajorMUD 1.11p
server: worlds, areas and quests written as TOML and applied on top of silvermere's stock world.
silvermere's `docs/overlays.md` describes the format.

| Overlay | What it is | Loads after |
| --- | --- | --- |
| [`mudrev`](mudrev/README.md) | The Realm of Legends' MudRev world, complete: everything it holds beyond the stock 1.11p world | — |
| [`ashfall-valley`](ashfall-valley/README.md) | A new area under the Volcano, levels 55–80, with a quest | `mudrev` |
| [`darkwood-quests`](darkwood-quests/README.md) | Darkwood BBS's 8th and 9th alignment quests (levels 150 and 200) | `mudrev` |
| [`gilded-asylum`](gilded-asylum/README.md) | The sealed wards above the Padded Cells, levels 100–150, with a quest | `mudrev` |
| [`rocspire`](rocspire/README.md) | Roc-haunted spires past Gloomy Mountain's Pinnacle, levels 150–200, with a class quest | `mudrev` |
| [`ossuary-court`](ossuary-court/README.md) | A court of bone and ash beneath Lord Magnus's hut, levels 200–250, with a party raid and the alignment quests' 10th step | `mudrev`, `darkwood-quests` |

## Using them

List the overlays in silvermere's settings, and every `silvermere import` (so also the stock world
a first start builds) applies them, in load order:

```toml
[content]
overlays = ["silvermere-overlays/mudrev", "silvermere-overlays/ashfall-valley"]
```

```
silvermere import                       # the stock world, then the overlays
silvermere overlay check                # what they would change, without writing
silvermere overlay apply                # apply them to a world already built (server stopped)
```

`mudrev` stands alone. The others are written against the MudRev world and say so with
`after = ["mudrev"]`.

## Layout

- Each overlay folder holds `overlay.toml` and its content files. Some have a `source/` folder
  that generates them; edit there and regenerate, as their READMEs say.
- `tools/area-survival/`: the survival check used to set an area's level band. It runs MajorMUD
  Explorer's combat model (through mudtool's port) for real characters against an area's monsters.
- `docs/content-areas.md`: the survey of the realm's level bands, and the design of the areas
  planned beyond Ashfall Valley.

## Credits

This repository builds on other people's work, and is shared in the same spirit as the releases
it comes from.

- **MajorMUD**, by Metropolis, Inc.: the game, and the stock 1.11p world every overlay here sits
  on. The stock world is not in this repository; silvermere fetches the MBBSEmu distribution of
  it.
- **MudRev**, the community's revised MajorMUD world. The `mudrev` overlay is the Realm of
  Legends' MudRev 1.11p data, exported as it ran on that realm.
  - Darkwood BBS's notes trace their MudRev to "Silicon's edits dated 9/25/2010".
  - We have not found a full list of MudRev's authors. If you are one, or know who they are,
    please open an issue so they can be named here.
- **Darkwood BBS** (DarkwoodBBS, `telnet://darkwood.ddns.net`): the 8th and 9th alignment quests.
  `darkwood-quests` takes their records and scripts from Darkwood's MajorMUD Explorer export,
  release DWBBS 1.5.0 (2020-09-18).
  - Darkwood's own release notes credit **EpicRev** ("Epic") for the class, item, spell,
    monster, race, shop, room and text data it merged.
  - They credit **Silicon** for the MudRev base.
  - They thank **Syntax** for the information on where to hex edit.
  - The export carries no prose, so the quests' conversations here are newly written for this
    repository, to fit Darkwood's scripts.
- **Syntax** (syntax53), for MajorMUD Explorer:
  - The `darkwood-quests` converter reads MME's export format and column meanings.
  - The survival check in `tools/area-survival` uses MME's combat and exp/hour formulas,
    through mudtool's port of it.
- **Ashfall Valley** is new content for the Realm of Legends. It gives a home to MudRev records
  that no room ever used (its dinosaurs, the Viperhide armour set) and is otherwise original.

The upstream releases state no license for their data, and this repository adds none. If you
want to use the data elsewhere, ask its original authors. Credits are as complete as we could
make them, so please open an issue if someone is missing or misnamed.
