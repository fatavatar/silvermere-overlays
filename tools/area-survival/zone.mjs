// Whether each character survives each zone of a new area, by MME's IsMobKillable (mudtool's
// port of MajorMUD Explorer), with the area's monsters as the world holds them after its overlay.
//   node zone.mjs chars.json monsters.json zones.json
// chars.json: export.py's output (its `chars`); monsters.json: export_monsters.py's; zones.json:
// { zone: { mons: [n...], max: k } }. A zone is judged as rooms holding `max` of its monsters
// at once: their damage while they fall one by one, and all their hit points.
import { readFileSync } from 'fs';
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
const { ATTACK, damageVsMonster } = await import(T + 'mmud/combat.js');
const { spellDoesDamage } = await import(T + 'mmud/details.js');
const X = await import(T + 'mmud/exphr.js');
const H = await import(T + 'hooks/combat.js');

await loadDB(MUDTOOL + '/data/', p => JSON.parse(readFileSync(p, 'utf8')));
detectEngine(db.info);
setSetting('globalFilter', true);

const [charsFile, monsFile, zonesFile] = process.argv.slice(2);
const chars = JSON.parse(readFileSync(charsFile, 'utf8')).chars;
const mons = JSON.parse(readFileSync(monsFile, 'utf8'));
const zones = JSON.parse(readFileSync(zonesFile, 'utf8'));

// the area's monsters into MME's rows: the realm's row where there is one, else a copy of a
// realm row the new monster was made from (its attacks and abilities are replaced anyway)
const KIND = { None: 0, Normal: 1, Spell: 2, Rob: 3 };
for (const [n, m] of Object.entries(mons)) {
  const num = +n;
  let row = by.monster.get(num);
  if (!row) {
    row = { ...db.Monsters[0], Number: num };
    db.Monsters.push(row);
    by.monster.set(num, row);
  }
  Object.assign(row, { Name: m.name, HP: m.maxhp, ArmourClass: m.ac, DamageResist: m.dr, MagicRes: m.magicres,
    EXP: m.exp, ExpMulti: m.level, Energy: m.energy, HPRegen: m.hpregen, RegenTime: m.regenhrs, BSDefense: m.bsdefense });
  for (let i = 0; i < 10; i++) {
    const [a, v] = (m.abilities || [])[i] || [0, 0];
    Object.assign(row, { [`Abil-${i}`]: a, [`AbilVal-${i}`]: v });
  }
  let prev = 0;
  for (let i = 0; i < 5; i++) {
    const a = m.attacks.find((_, j) => j === i) || { kind: 0, accuracy: 0, pct: 0, min: 0, max: 0, energy: 0, hitspell: 0 };
    const kind = typeof a.kind === 'string' ? KIND[a.kind] : a.kind;
    Object.assign(row, { [`AttType-${i}`]: kind, [`AttAcc-${i}`]: a.accuracy, [`Att%-${i}`]: a.pct,
      [`AttTrue%-${i}`]: kind ? Math.max(0, a.pct - prev) : 0, [`AttMin-${i}`]: a.min, [`AttMax-${i}`]: a.max,
      [`AttEnergy-${i}`]: a.energy, [`AttHitSpell-${i}`]: a.hitspell });
    if (kind) prev = a.pct;
  }
}

function build(c, attack) {
  const ch = blankChar();
  Object.assign(ch, { name: c.name, cls: c.cls, race: c.race, level: c.level, stats: { ...c.stats } });
  for (const it of c.worn) if (by.item.get(it)) equipItem(ch, it, { toggle: false });
  if (c.weapon && by.item.get(c.weapon)) ch.equipped[16] = c.weapon;
  ch.learnedSpells = c.spells.slice();
  ch.attack = { ...ch.attack, healType: 1, ...attack };
  return ch;
}

function judge(c, attack) {
  const ch = build(c, attack);
  addChar(ch);
  const panel = calcCharStats(ch, { globalFilter: true });
  const summary = calcCharSummary(ch, panel);
  const cp = profileFromChar(ch, { globalFilter: true });
  const hc = X.expHrCharacter(ch, { useChar: true, profile: cp, panel, summary });
  const profile = X.expHrProfile(cp, true, hc.spellOverhead);
  const at = X.attackConfig(ch.attack, ch.equipped);
  const verdict = {};
  for (const [zone, z] of Object.entries(zones)) {
    let ok = 0;
    const detail = [];
    for (const n of z.mons) {
      const m = by.monster.get(n);
      const out = damageVsMonster(profile, at, m).averageDamage;
      const inc = H.calcMonsterDamage(n).avg;
      const k = z.max || 1;
      const live = X.isMobKillable(out, hc.hp, inc * (k + 1) / 2, m.HP * k, hc.hpRegen, m.HPRegen * k);
      if (live) ok++;
      detail.push({ n, name: m.Name, out: Math.round(out), in: Math.round(inc), ok: live });
    }
    verdict[zone] = { share: ok / z.mons.length, detail };
  }
  return { verdict, hp: hc.hp };
}

const rows = [];
for (const c of chars) {
  const attacks = [{ type: ATTACK.weapon }];
  for (const s of c.spells) if (by.spell.get(s) && spellDoesDamage(s, true)) attacks.push({ type: ATTACK.spell, spellNum: s, spellLvl: c.level });
  let best = null;
  for (const a of attacks) {
    const r = judge(c, a);
    const score = Object.values(r.verdict).reduce((t, v) => t + v.share, 0);
    if (!best || score > best.score) best = { score, ...r };
  }
  rows.push({ name: c.name, level: c.level, hp: best.hp, verdict: best.verdict });
}
rows.sort((a, b) => a.level - b.level);
const zs = Object.keys(zones);
console.log('char'.padEnd(12), 'lvl', '  hp', zs.map(z => z.padStart(8)).join(''));
for (const r of rows) {
  console.log(r.name.padEnd(12), String(r.level).padStart(3), String(r.hp).padStart(5),
    zs.map(z => (Math.round(r.verdict[z].share * 100) + '%').padStart(8)).join(''));
}
if (process.env.DETAIL) {
  for (const r of rows.filter(r => r.name === process.env.DETAIL)) console.log(JSON.stringify(r.verdict, null, 1));
}
