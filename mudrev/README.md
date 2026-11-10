# MudRev (Realm of Legends) as an overlay

The realm's whole content as a silvermere content overlay: everything the realm holds beyond
silvermere's stock 1.11p world. A stock import plus this overlay gives the realm's rooms,
monsters, items, spells, shops, messages, texts, classes, races and actions exactly, and its
help, gang-house descriptions and login texts, with no MudRev data files (`.DAT`/`.VIR`/`.MDB`)
or message files.

**Generated; do not edit by hand.** Make content changes in their own overlays (like
`../ashfall-valley`, with `after = ["mudrev"]`), so this one stays a plain copy of the realm.

## Credits

- **MudRev**, the community's revised MajorMUD world, which this is. Darkwood BBS's notes trace
  their MudRev to "Silicon's edits dated 9/25/2010". We have not found a full list of MudRev's
  authors; please open an issue if you can name them.
- **MajorMUD** by Metropolis, Inc., the stock world this sits on (not included here).
- **The Realm of Legends**, whose MudRev 1.11p data this was exported from.

## How it was made

```
silvermere import --database-url sqlite://stock.db                 # the stock world
silvermere overlay export --database-url sqlite://realm.db \
    --base sqlite://stock.db --name mudrev --out mudrev
```

`realm.db` was the Realm of Legends as silvermere imported it from the realm's live `.DAT`
files (2026-11-09), before any overlay.

| | New | Changed from stock |
| --- | ---: | ---: |
| Rooms | 45,851 | 24,896 |
| Monsters | 400 | 1,101 |
| Items | 1,228 | 1,361 |
| Spells | 627 | 1,314 |
| Shops | 123 | 178 |
| Messages | 513 | 174 |
| Texts | 535 | 438 |
| Classes | 10 | 15 |
| Races | 5 | 13 |
| Actions | 27 | 0 |
| Help topics | 0 | 88 |
| Description files | 86 | 0 |
| Game texts | 0 | 2 |

The help topics, description files and game texts (`help.toml`, `desc_files.toml`,
`game_texts.toml`) were added on 2026-11-10, exported the same way once silvermere kept them as
content: the realm's rewritten help (`WCCMMHLP.MSG`), its 86 gang-house `.HSE` files beyond
stock's, and its login line (`USRLOGIN`) and entry banner (`USRFOLED`) from `WCCMMUD.MSG`. The
other files were left as they were. A full re-export would also drop the shops' stock on hand
(`qty`), which is play, not content.

`overlay.toml` sets `references = "warn"`: the realm has 272 numbers that point at nothing (most
are item hit messages of 8224, two bytes of spaces left in unused fields), and a copy keeps them.

## How it was checked

- Stock plus this overlay, exported against the realm, differs in nothing, and every content
  table matches the realm's row for row (surrogate row ids aside).
- A fresh `silvermere import` with `content.overlays = [ashfall-valley, mudrev]` builds a world
  whose content equals the running realm's (which has Ashfall Valley applied).
