from lib.utilities import (
    loadSave,
    writeSave,
    loadConfig,
    nestedMenuOptions,
    menuOptions,
    directFunction,
    promptInt,
    promptStr,
    const,
    getProfiles,
    loadItems
)
from random import randint


@directFunction
def setMoney():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    amount = promptInt('Set money amount: ', minValue=0)
    userData['Inventory'][profile]['Money'] = amount
    writeSave(userData)
    return f'Set {amount:,}$ to {profile}'


@directFunction
def setLevel():
    XP_ARR = [
        0, 1071, 1288, 1655, 2176, 2855, 3696, 4704, 5883, 7237, 8770, 10486, 12390, 
        14486, 16778, 19270, 21966, 24871, 27989, 31324, 34880, 38661, 42672, 46917, 
        51400, 56125, 91145, 98978, 107193, 115797, 124795, 134195, 144002, 154222, 
        164863, 175930, 187430, 199368, 211752, 224587, 237880, 251637, 265865, 280569, 
        295756, 311433, 327605, 344279, 361461, 379158, 397375, 416120, 435398, 455215, 
        475579, 496495, 517970, 540009, 562620, 585808, 609580, 844923, 878201, 912282, 
        947176, 982890, 1019433, 1056813, 1095038, 1134118, 1174060, 1214873, 1256565, 
        1299144, 1342620, 1387000, 1432293, 1478507, 1525650, 1573732, 1622760, 1672743, 
        1723689, 1775606, 1828504, 1882390, 1937273, 1993161, 2050062, 2107986, 2166940, 
        3339899, 3431459, 3524603, 3619342, 3715690, 3813659, 3913262, 4014512, 4117420]

    userData = loadSave()
    level = promptInt('Set level (0-100): ', minValue=0, maxValue=100)
    total = sum(XP_ARR[:level])
    profile = loadConfig()['current_profile']
    userData['Inventory'][profile]['Skills']['PlayerLevel'] = level
    userData['Inventory'][profile]['Skills']['PlayerTotalXp'] = total
    writeSave(userData)
    return f"Set profile level to {level}"


@directFunction
def setBlackKeys():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    amount = promptInt('Set black keys amount: ', minValue=0)
    userData['Inventory'][profile]['Skills']['AvailableBlackKeys'] = amount
    writeSave(userData)
    return f'Set {amount:,} black keys to {profile}'


@directFunction
def setAugCores():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    amount = promptInt('Set augment cores amount: ', minValue=0)
    userData['Inventory'][profile]['Skills']['AvailableEliteAugmentCores'] = amount
    writeSave(userData)
    return f'Set {amount:,} augment cores to {profile}'


@directFunction
def setRandBlackStrongbox():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    amount = promptInt('Set black strongboxes amount: ', minValue=0)
    userData['Inventory'][profile]['Skills']['AvailableBlackStrongboxes'] = ([randint(100000, 99999999999) for _ in range(amount)])
    writeSave(userData)
    return f'Set {amount:,} black strongboxes to {profile}'


@directFunction
def activateSkillReset():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    userData['Inventory'][profile]['FreeSkillsReset'] = not userData['Inventory'][profile]['FreeSkillsReset']
    writeSave(userData)
    return f'{'Activated free skill reset' if not userData['Inventory'][profile]['FreeSkillsReset'] else 'Deactivated free skill reset'}'


@directFunction
def changeUsername():
    userData = loadSave()
    profile = loadConfig()['current_profile']
    name = promptStr('Set new name: ')
    userData['Inventory'][profile]['Name'] = name
    writeSave(userData)
    return f'Name set to: {name}'

@menuOptions
def setGrenades(grenade: str = '__menu_options__'):
    GRENADES = [
        ('Cryo grenades', 'grenades_cryo'),
        ('Frag grenades', 'grenades_frag')
    ]

    if grenade == '__menu_options__':
        return [f"{g[0]}" for g in GRENADES]
    
    userData = loadSave()
    profile = loadConfig()['current_profile']

    optionName, identifier = next(((g[0], g[1]) for g in GRENADES if f"{g[0]}" == grenade), (None, None))
    
    amount = promptInt(f'Enter amount of {optionName}: ')
    userData['Inventory'][profile]['Ammo'][identifier] = amount
    writeSave(userData)
    return f'{optionName} set to {amount:,}'


@menuOptions
def deleteProfile(profile: str = '__menu_options__'):
    PROFILES = getProfiles()
    
    if profile == '__menu_options__':
        return PROFILES

    userData = loadSave()
    userData['Inventory'][profile] = {"Loaded": False}
    writeSave(userData)
    return f'Profile {profile} has been deleted'


@menuOptions
def setTurrets(turret: str = '__menu_options__'):
    turretItems = loadItems()['turret']
    userData = loadSave()
    profile = loadConfig()['current_profile']
    turretType = 'normal' if userData['Inventory'][profile]['Skills']['PlayerLevel'] <= 30 else 'red'
    TURRETS = [(t['Name'], t['ID']) for t in turretItems[turretType]]

    if turret == '__menu_options__':
        return [t[0] for t in TURRETS]

    optionName, turretID = next(((t[0], t[1]) for t in TURRETS if t[0] == turret), (None, None))
    amount = promptInt(f'Set {optionName} turrets amount: ', minValue=0)
    
    for i in userData['Inventory'][profile]['Turrets']:
        if i.get('TurretId') == turretID:
            i['TurretCount'] = amount
            break
    else:
        userData['Inventory'][profile]['Turrets'].append({'TurretId': turretID, 'TurretCount': amount})
    return f'{optionName} turret amount set to: {amount}'


@nestedMenuOptions
def setStdWeapons(weaponType: str = '__menu_options__'):
    items = loadItems()

    if weaponType == '__menu_options__':
        return {w.capitalize().replace('_', ' '): setStdWeapons for w in items['weapons'].keys()}

    def setWeaponVersion(version: str = '__menu_options__'):
        if version == '__menu_options__':
            return {v.capitalize(): setWeaponVersion for v in items['weapons'][weaponType.lower().replace(' ', '_')].keys()}
        
        WEAPONS = items['weapons'][weaponType.lower().replace(' ', '_')][version.lower()]
        
        def setWeapon(weapon: str = '__menu_options__'):
            if weapon == '__menu_options__':
                return {w['Name']: setWeapon for w in WEAPONS}

            selectedWeapon = next((w for w in WEAPONS if w['Name'] == weapon), None)
            if selectedWeapon:
                userData = loadSave()
                profile = loadConfig()['current_profile']
                weaponID = selectedWeapon['ID']
                bonus = promptInt('Set item bonus stats [0-10]: ', minValue=0, maxValue=10)
                augments = promptInt('Set item augments [0-4]: ', minValue=0, maxValue=4)
                grade = promptInt('Set item grade [0-12]: ', minValue=0, maxValue=12)
                
                strongbox = {
                    "ID": weaponID,
                    "EquipVersion": {'normal': 0, 'red': 1, 'black': 2, 'factions': 3}.get(version, 0),
                    "Grade": grade,
                    "EquippedSlot": -1,
                    "AugmentSlots": augments,
                    "InventoryIndex": 0,
                    "Seen": False,
                    "BonusStatsLevel": bonus,
                    "ContainsKey": False,
                    "ContainsAugmentCore": False,
                    "BlackStrongboxSeed": 0,
                    "UseDefaultOpenLogic": True
                }
                
                userData['Inventory'][profile]['Strongboxes']['Claimed'].extend([0, strongbox, 8, 2])
                
                writeSave(userData)
                return f'{weapon} ({version}) added to strongboxes with bonus: {bonus}, augments: {augments}, grade: {grade}'
            
        return setWeapon()

    return setWeaponVersion()


@nestedMenuOptions
def setArmour(armourType = '__menu_options__'):
    items = loadItems()

    if armourType == '__menu_options__':
        return {a.capitalize().replace('_', ' '): setArmour for a in items['armour'].keys()}

    def setArmourVersion(version: str = '__menu_options__'):
        if version == '__menu_options__':
            return {v.capitalize(): setArmourVersion for v in items['armour'][armourType.lower().replace(' ', '_')].keys()}
        
        ARMOUR = items['armour'][armourType.lower().replace(' ', '_')][version.lower()]
        
        def setArmourItem(armour: str = '__menu_options__'):
            if armour == '__menu_options__':
                return {a['Name']: setArmourItem for a in ARMOUR}

            selectedWeapon = next((a for a in ARMOUR if a['Name'] == armour), None)
            if selectedWeapon:
                userData = loadSave()
                profile = loadConfig()['current_profile']
                armourID = selectedWeapon['ID']
                bonus = promptInt('Set item bonus stats [0-10]: ', minValue=0, maxValue=10)
                augments = promptInt('Set item augments [0-4]: ', minValue=0, maxValue=4)
                grade = promptInt('Set item grade [0-12]: ', minValue=0, maxValue=12)
                
                strongbox = {
                    "ID": armourID,
                    "EquipVersion": {'normal': 0, 'red': 1, 'black': 2, 'factions': 3}.get(version, 0),
                    "Grade": grade,
                    "EquippedSlot": {'helmet': 1, 'vest': 2, 'gloves': 3, 'boots': 4, 'pants': 5}.get(armourType.lower(), 0),
                    "AugmentSlots": augments,
                    "InventoryIndex": -1,
                    "Seen": False,
                    "BonusStatsLevel": bonus,
                    "Equipped": False, 
                    "ContainsKey": False,
                    "ContainsAugmentCore": False,
                    "BlackStrongboxSeed": 0,
                    "UseDefaultOpenLogic": True
                }
                
                userData['Inventory'][profile]['Strongboxes']['Claimed'].extend([1, strongbox, 8, 2])
                
                writeSave(userData)
                return f'{armour} ({version}) added to strongboxes with bonus: {bonus}, augments: {augments}, grade: {grade}'
            
        return setArmourItem()

    return setArmourVersion()


@nestedMenuOptions
def setPremiumWeapons(weaponType: str = '__menu_options__'):
    items = loadItems()

    if weaponType == '__menu_options__':
        return {w.capitalize().replace('_', ' '): setPremiumWeapons for w in items['premium'].keys()}

    WEAPONS = items['premium'][weaponType.lower().replace(' ', '_')]

    def setPremWeapon(weapon: str = '__menu_options__'):
        if weapon == '__menu_options__':
            return {w['Name']: setPremWeapon for w in WEAPONS}

        selectedWeapon = next((w for w in WEAPONS if w['Name'] == weapon), None)
        if selectedWeapon:
            userData = loadSave()
            profile = loadConfig()['current_profile']
            for i in userData['PurchasedIAP']['PurchasedIAPArray']:
                if i['Identifier'] == f'sas4_{selectedWeapon['Name'].lower().replace(' ', '')}':
                    i['Value'] = not i['Value']
            weaponID = selectedWeapon['ID']
            bonus = promptInt('Set item bonus stats [0-10]: ', minValue=0, maxValue=10)
            augments = promptInt('Set item augments [0-4]: ', minValue=0, maxValue=4)
            grade = promptInt('Set item grade [0-12]: ', minValue=0, maxValue=12)
            
            strongbox = {
                "ID": weaponID,
                "EquipVersion": 0,
                "Grade": grade,
                "EquippedSlot": -1,
                "AugmentSlots": augments,
                "InventoryIndex": 0,
                "Seen": False,
                "BonusStatsLevel": bonus,
                "ContainsKey": False,
                "ContainsAugmentCore": False,
                "BlackStrongboxSeed": 0,
                "UseDefaultOpenLogic": True
            }
            
            userData['Inventory'][profile]['Strongboxes']['Claimed'].extend([0, strongbox, 8, 2])
            
            writeSave(userData)
            return f'{weapon} added to strongboxes with bonus: {bonus}, augments: {augments}, grade: {grade}'
        
    return setPremWeapon()


PROFILE = {
    'Set items': {
        'Set weapons': {
            'Set standard weapons': setStdWeapons,
            'Set premium weapons': setPremiumWeapons
        },
        'Set armour': setArmour,
        'Set turrets': setTurrets,
        'Set grenades': setGrenades
    },
    'Set money': setMoney,
    'Set level': setLevel,
    'Set black keys': setBlackKeys,
    'Set augment cores': setAugCores,
    'Add random black strongbox': setRandBlackStrongbox,
    'Activate free skill reset': activateSkillReset,
    'Change name': changeUsername,
    'Delete a profile': deleteProfile,
    'Unlock collections': ...,
}