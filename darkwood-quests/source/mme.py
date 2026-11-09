"""MajorMUD Explorer's columns as silvermere record fields: the translation the Darkwood
converter uses. verify.py checks it against every realm record both sides hold."""

# MME column -> silvermere field, for the plain numbers. Codes keep their number here;
# ENUMS says which fields are written by name.
MONSTER = {
    'Weapon': 'weapon', 'ArmourClass': 'ac', 'DamageResist': 'dr', 'Follow%': 'followpct',
    'MagicRes': 'magicres', 'BSDefense': 'bsdefense', 'EXP': 'exp', 'ExpMulti': 'level',
    'HP': 'maxhp', 'Energy': 'energy', 'GreetTXT': 'talktext', 'HPRegen': 'hpregen',
    'CharmLVL': 'charmlvl', 'Type': 'grouprole', 'Undead': 'undead', 'Align': 'alignment',
    'RegenTime': 'regenhrs', 'DeathSpell': 'deathspell', 'CreateSpell': 'createspell',
    'Name': 'name',
}
MONSTER_CASH = {'R': 'runic', 'P': 'platinum', 'G': 'gold', 'S': 'silver', 'C': 'copper'}
ITEM = {
    'Limit': 'limit', 'Encum': 'weight', 'ItemType': 'item_type', 'UseCount': 'charges',
    'Price': 'cost', 'Currency': 'currency', 'Min': 'mindmg', 'Max': 'maxdmg',
    'ArmourClass': 'ac', 'DamageResist': 'dr', 'WeaponType': 'wpntype',
    'ArmourType': 'armtype', 'Worn': 'worn', 'Accy': 'accuracy', 'Gettable': 'gettable',
    'StrReq': 'strreq', 'Speed': 'speed', 'Not Droppable': 'nodrop',
    'Destroy On Death': 'destroy', 'Retain After Uses': 'retain', 'Name': 'name',
}
SPELL = {
    'ReqLevel': 'level', 'EnergyCost': 'energy', 'ManaCost': 'mana', 'MinBase': 'minval',
    'MaxBase': 'maxval', 'Diff': 'diff', 'TypeOfResists': 'resmode', 'Targets': 'target',
    'Dur': 'duration', 'AttType': 'element', 'Magery': 'magery', 'MageryLVL': 'magelvl',
    'Cap': 'levelcap', 'MaxIncLVLs': 'maxlvls', 'MaxInc': 'maxinc', 'MinIncLVLs': 'minlvls',
    'MinInc': 'mininc', 'DurIncLVLs': 'durlvls', 'DurInc': 'durinc', 'Name': 'name',
    'Short': 'shortnm',
}
# fields written by name, and their enum
ENUMS = {
    'grouprole': 'GroupRole', 'alignment': 'Alignment', 'item_type': 'ItemType',
    'currency': 'Currency', 'wpntype': 'WeaponType', 'armtype': 'ArmourType',
    'worn': 'WornLocation', 'resmode': 'ResistMode', 'target': 'SpellTarget',
    'element': 'Element', 'magery': 'Magery',
}
# the db column where it differs from the field name
COLUMN = {'group': 'group_num', 'limit': 'limit_copies'}


def abilities(row, n=20):
    """[(code, value)] of the used ability slots, in slot order."""
    return [(row[f'Abil-{i}'], row[f'AbilVal-{i}']) for i in range(n)
            if row.get(f'Abil-{i}')]


def attacks(row):
    """[{kind, accuracy, pct, min, max, energy, hitspell}] of the used attack slots."""
    out = []
    for i in range(5):
        if not row.get(f'AttType-{i}'):
            continue
        out.append(dict(kind=row[f'AttType-{i}'], accuracy=row[f'AttAcc-{i}'], pct=row[f'Att%-{i}'],
                        min=row[f'AttMin-{i}'], max=row[f'AttMax-{i}'], energy=row[f'AttEnergy-{i}'],
                        hitspell=row[f'AttHitSpell-{i}']))
    return out


def monster_spells(row):
    return [dict(spell=row[f'MidSpell-{i}'], pct=row[f'MidSpell%-{i}'], level=row[f'MidSpellLVL-{i}'])
            for i in range(5) if row.get(f'MidSpell-{i}') or row.get(f'MidSpell%-{i}')]


def drops(row):
    return [dict(item=row[f'DropItem-{i}'], pct=row[f'DropItem%-{i}'])
            for i in range(10) if row.get(f'DropItem-{i}')]


def lists(row, prefix, n=10):
    return [row[f'{prefix}{i}'] for i in range(n) if row.get(f'{prefix}{i}')]
