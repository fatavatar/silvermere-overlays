# Darkwood quests (the 8th and 9th alignment quests)

Darkwood BBS's two extra alignment quests (levels 150 and 200) as a silvermere content overlay.
The files here are generated: the source is `source/package` (its README explains the quests and
the choices made), converted by `source/convert.py`.

```
REALM_DB=... SILVERMERE_SRC=... python3 source/convert.py     # regenerate after editing the source
silvermere overlay check darkwood-quests
silvermere overlay apply darkwood-quests                      # stop the server first
```

## Credits

- **The quests themselves**: [Darkwood BBS](telnet://darkwood.ddns.net) (DarkwoodBBS). The
  records and scripts come from Darkwood's MajorMUD Explorer export, release DWBBS 1.5.0
  (2020-09-18), whose release notes record the quests as Darkwood's 1.0.x (8th) and 1.2.x (9th)
  work. Darkwood's data builds on EpicRev's and Silicon's MudRev work.
- **The conversations**: Darkwood's export carries no prose, so the text in `text.toml` was
  newly written for this repository to fit Darkwood's scripts (`source/package/text.toml`).
- **The column translation**: MajorMUD Explorer's export format, by Syntax (syntax53).

## What the conversion does

- **Columns.** The Darkwood file's MajorMUD Explorer columns become silvermere record fields
  (`source/mme.py`). `source/verify.py` checks the translation against every realm record
  that both the realm database and its MME export hold: all 1,501 monsters, 3,178 items and
  2,006 spells agree, apart from three known differences in how values are stored (a
  monster's backstab defence and a spell's level cap keep only their low byte, and one item
  writes "no class" as 65535).
- **What the file lacks** comes from the realm. A new record starts from the realm record it
  was modelled on: the false King takes the realm King's attack messages (hit, armour
  deflect, dodge), and each new spell starts from a realm spell of the same kind.
- **Exits.** A locked door is a gate exit that cannot be picked; an exit to another map is
  a map-change exit.
- **Scripts.** The six realm scripts the quests extend (Chancellor Annora, The Grey Lord,
  Balthazar) are taken over whole with `replace = true`, keeping their realm links. A prose
  block's link is recovered from its callers; all 119 links match the Darkwood file.
- **Text markup.** The drafts' keywords, goal lines and experience lines are written in the
  realm's colours.

## How it was checked

- `overlay check` against a copy of the Realm of Legends (with Ashfall Valley applied): every `was`
  matched, every number it names exists, and it shares no record with Ashfall.
- In a test server on that copy:
  - The Grey Lord refuses an under-level character with his "grow further" message.
  - The starmetal giant king's greeting and "protection" topic advance the neutral quest
    from step 47 to 48 and show the goal line.
  - The mirror in the castle guard tower leads to the false King's throne room, where he
    attacks on sight. (The way back was not tried: the test character was stunned.)

Not on the live realm yet.
