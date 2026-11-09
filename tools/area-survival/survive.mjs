// Which areas each character can survive, by MME's own rules (mudtool's port of MajorMUD Explorer):
// its exp/hr pipeline returns -1 when IsMobKillable says the character dies first. Input from export.py.
import { readFileSync, writeFileSync } from 'fs';
// MUDTOOL: a checkout of mudtool, the browser port of MajorMUD Explorer
const MUDTOOL = process.env.MUDTOOL;
if (!MUDTOOL) throw new Error('set MUDTOOL to a mudtool checkout');
const T = MUDTOOL + '/js/';
const { loadDB, db, by } = await import(T + 'db.js');
const { detectEngine } = await import(T + 'mmud/engine.js');
const { blankChar, addChar } = await import(T + 'char.js');
const { setSetting } = await import(T + 'state.js');
const { calcCharStats, calcCharSummary, equipItem } = await import(T + 'mmud/charstats.js');
const { profileFromChar } = await import(T + 'mmud/profile.js');
const { ATTACK } = await import(T + 'mmud/combat.js');
const { lairAverages, spellDoesDamage } = await import(T + 'mmud/details.js');
const X = await import(T + 'mmud/exphr.js');
const H = await import(T + 'hooks/combat.js');

await loadDB(MUDTOOL + '/data/', p => JSON.parse(readFileSync(p, 'utf8')));
detectEngine(db.info);
setSetting('globalFilter', true);

const IN = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const pool = new Set();
for (const a of Object.values(IN.areas)) { for (const n of Object.keys(a.mons)) pool.add(+n); for (const n of a.spec) pool.add(n); }
const mons = [...pool].map(n => by.monster.get(n)).filter(Boolean);

function build(c, attack) {
  const ch = blankChar();
  Object.assign(ch, { name: c.name, cls: c.cls, race: c.race, level: c.level, stats: { ...c.stats } });
  for (const it of c.worn) if (by.item.get(it)) equipItem(ch, it, { toggle: false });
  if (c.weapon && by.item.get(c.weapon)) ch.equipped[16] = c.weapon;   // the wielded weapon is kept apart from worn gear
  ch.learnedSpells = c.spells.slice();
  ch.attack = { ...ch.attack, healType: 1, ...attack };   // no healing assumed
  return ch;
}
function envFor(ch) {
  addChar(ch);
  const panel = calcCharStats(ch, { globalFilter: true });
  const summary = calcCharSummary(ch, panel);
  const cp = profileFromChar(ch, { globalFilter: true });
  const hc = X.expHrCharacter(ch, { useChar: true, profile: cp, panel, summary });
  const lairs = new Map();
  return { panel, env: { ch: hc, profile: X.expHrProfile(cp, true, hc.spellOverhead), attack: X.attackConfig(ch.attack, ch.equipped),
    config: X.normaliseExpHrConfig({}), useChar: true,
    lair: sb => { if (!lairs.has(sb)) lairs.set(sb, lairAverages(sb)); return lairs.get(sb); },
    monsterDamage: mon => H.calcMonsterDamage(mon.Number).avg } };
}
function run(c, attack) {
  const { panel, env } = envFor(build(c, attack));
  const out = {};
  for (const m of mons) {
    let r; try { r = X.monsterExpPerHour(m, env); } catch (e) { r = null; }
    if (r && r.info) out[m.Number] = Math.round(r.info.nExpPerHour);
  }
  return { out, hp: env.ch.hp };
}
const result = {};
for (const c of IN.chars) {
  const attacks = [{ type: ATTACK.weapon }];
  for (const s of c.spells) {
    const sp = by.spell.get(s);
    if (sp && spellDoesDamage(s, true)) attacks.push({ type: ATTACK.spell, spellNum: s, spellLvl: c.level });
  }
  let best = null;
  for (const a of attacks) {
    const r = run(c, a);
    const ok = Object.values(r.out).filter(v => v > 0).length;
    if (!best || ok > best.ok) best = { ok, attack: a, ...r };
  }
  result[c.name] = { level: c.level, cls: c.cls, hp: best.hp, attack: best.attack, killable: best.ok, exphr: best.out };
  console.error(c.name, c.level, 'attack', JSON.stringify(best.attack), 'hp', best.hp, 'killable', best.ok, '/', mons.length);
}
writeFileSync(process.argv[3], JSON.stringify(result));
