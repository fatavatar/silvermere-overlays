# Darkwood's 8th and 9th alignment quests

These files contain only what Darkwood's two extra alignment quests need, taken out of
`DarkwoodBBSMME.mdb` and nothing else from Darkwood. The numbers come word for word from the
MDB, and the text is from the drafts in `../darkwood`. Nothing loads these files yet.

Our realm's seven alignment quests start at levels 10, 20, 30, 40, 50, 75 and 100. Darkwood
continues each alignment's quest from step 47:

- **8th quest** (level 150, steps 47 to 53): kill two bosses and receive the Aura of Light, the
  Scales of Balance or the Icon of Evil.
- **9th quest** (level 200, steps 53 to 61): kill two more bosses, talk to the gaunt one weaver,
  then kill the Onyx Juggernaut and Lord Magnus. The reward item is upgraded.

## What is in here

| File | New | Changed realm records |
| --- | --- | --- |
| `scripts.toml` | 45 quest scripts | the three quest givers' talk and quest scripts gain their new lines (6 scripts) |
| `text.toml` | 68 conversations (drafted) | |
| `monsters.toml` | the false King of Nazareen | 16: three quest givers, the weaver, 12 bosses |
| `items.toml` | 10: the three rewards, their upgrades, the rune, globe and glyph, the mirror | |
| `spells.toml` | 38: the rewards' powers and the plumbing behind each kill step | |
| `rooms.toml` | the throne room behind the mirror and the room beyond its door | 14: the mirror room, 12 castle halls, the weaver's glade |
| `messages.toml` | 10 (mirror, globe, glyph, rune and reward messages) | |

Every number these records point at is either in these files or already in the realm. That
includes the messages a quest giver shows when you are under-level or the wrong alignment (for
example Balthazar's "I have work but not for one as puny as you!"). The realm already has them all.

### Changes to things we already have

Each change sets only what the quest needs:

- **Quest givers.** These monsters get a greeting that offers the new quest:
  - the temple healer (#1232) becomes **High Priest Annora** (good);
  - the **starmetal giant king** (#1321) (neutral);
  - the **Enigma Master** (#1205) (evil).
- **The gaunt one weaver** (#696) gets a greeting. He is placed in Dreary Forest (2/9808),
  because in our realm he exists but appears nowhere.
- **Bosses.** Each of these gets a death spell that moves the killer on a step:
  - Demonic Angel, Athos, Kryon Dragon (good);
  - Ancient Dragon, Atlas, Acid Beast, Ancient Phantasm (neutral);
  - Angelic Demon, starmetal giant king, Demonic Enchantress, Demon Lord (evil);
  - Onyx Juggernaut and Lord Magnus (all three).
- **Chancellor Annora, The Grey Lord and Balthazar.** Their scripts gain the new lines. Nothing in
  the realm's scripts is removed or reworded.
- **Castle of Nazareen:**
  - The Guard Tower (1/6024) gets the large mirror and the "go mirror" / "enter mirror" command.
  - The 12 halls from 1/6044 to 1/6055 send good characters on step 54 back to the gates, which
    pushes them to the mirror.

## Left out on purpose

Darkwood changes more than this on the same records. These changes are not part of the quests:

- **Coin and drop-rate changes** on the bosses, the quest givers and the trainers. These are
  Darkwood's economy rebalance.
- **Darkwood loot on the quest bosses:**
  - Sandals and Gloves of Fury (Enigma Master);
  - crystal tokens (Lord Magnus);
  - the Darkwood Shield (Demon Lord).
- **Other stat changes on those bosses:**
  - Lord Magnus's water resistance;
  - the Enigma Master's spells and alignment;
  - regeneration times.
- **The Enigma Master's death spell.** Darkwood removed it. We keep it, because our evil quest
  needs it at step 18 (killing the Enigma Master with the long golden chain).
- **The mirror command on Cracked Plain, Black Chasm (7/789).** This looks like a Darkwood slip,
  because that room has the same number as the throne room on map 3. It would let anyone on the
  plain step into the castle guard tower.

## Choices to review

1. **Two bosses lose their own death effect.**
   - The starmetal giant king loses chain lightning, and the Acid Beast loses its acid spray.
   - A monster has only one death spell, and Darkwood used it for the quest step.
   - Keeping both would need a spell that does both.
2. **The healer becomes High Priest Annora.** Her old healer greeting goes away. The healer's
   spells still say "The healer casts...".
3. The text choices listed in `../darkwood/README.md`:
   - the false King;
   - the castle halls turning good characters away;
   - the weaver's backstory;
   - the borrowed message templates.

## Layout

- Each file's header explains its records.
- New records list their fields under MME's column names, and fields left out are 0.
- Abilities are written as `[name, value]` pairs.
- Changed records give `set` (the new values) and `was` (the realm's current values). An importer
  can refuse to apply a change when the realm no longer matches.
