from lib.utilities import loadSave, writeSave, promptInt, directFunction, menuOptions, loadItems, nestedMenuOptions
from typing import Union, List


@menuOptions
def changeGuild(guild: str = "__menu_options__") -> Union[str, List[str]]:
    GUILDS = [
        "GUARDIANS",
        "NOMADS",
        "OUTLAWS",
        "SPARTANS",
        "CENTURIONS",
        "CORSAIRS",
        "RANGERS",
        "VANGUARD"
    ]

    if guild == "__menu_options__":
        return GUILDS
    
    if guild not in GUILDS:
        return f"Invalid guild: {guild}"
    
    userData = loadSave()
    userData['CurrentFactionWarFaction'] = guild
    writeSave(userData)
    return f"Changed guild to {guild}"


@menuOptions
def setCredits(planet: str = "__menu_options__") -> Union[str, List[str]]:
    PLANETS = [
        ('ZETA', 0),
        ('EPSILON', 1),
        ('SIGMA', 2),
        ('XI', 3),
        ('OMICRON', 4)
    ]

    if planet == "__menu_options__":
        return [f"{p[0]}" for p in PLANETS] + ["ALL", "FACTION WAR"]
    
    userData = loadSave()
    
    if planet == "FACTION WAR":
        amount = promptInt("Enter the amount of FactionWarCredits: ")
        userData['FactionWarCredits'] = amount
        writeSave(userData)
        return f"Set FactionWarCredits to {amount}"
    
    if planet == "ALL":
        amount = promptInt("Enter the amount of credits for all planets: ")
        for p in userData['FactionWarPlanetArray']:
            p['Currency'] = amount
    else:
        planet_name, planet_index = next(((p[0], p[1]) for p in PLANETS if f"{p[0]}" == planet), (None, None))
        if planet_index is None:
            return f"Invalid planet: {planet}"
        amount = promptInt(f"Enter the amount of credits for {planet_name}: ")
        userData['FactionWarPlanetArray'][planet_index]['Currency'] = amount
    
    writeSave(userData)
    return f"Set credits for {'all planets' if planet == 'ALL' else planet_name} to {amount}"


@menuOptions
def unlockProfiles(profile: str = '__menu_options__'):
    PROFILES = [
        ('IAP Character slot 1', 'SAS4_CharacterSlot1'),
        ('IAP Character slot 2', 'SAS4_CharacterSlot2')
    ]

    if profile == '__menu_options__':
        return [f"{p[0]}" for p in PROFILES]
    
    userData = loadSave()
    optionName, identifier = next(((p[0], p[1]) for p in PROFILES if f"{p[0]}" == profile), (None, None))
    for i in userData['PurchasedIAP']['PurchasedIAPArray']:
        if i['Identifier'] == identifier:
            i['Value'] = not (i['Value'])
            writeSave(userData)
            return f'Profile: {optionName} was {'activated' if i['Value'] else 'deactivated'}'


@directFunction
def unlockFairground():
    userData = loadSave()
    for i in userData['PurchasedIAP']['PurchasedIAPArray']:
        if i['Identifier'] == 'sas4_fairgroundpack':
            i['Value'] = not (i['Value'])
            if i['Identifier'] == 'sas4_fairgroundpacksale':
                i['Value'] = not (i['Value'])
            writeSave(userData)
            return f'{'Activated fairground pack' if i['Value'] else 'Deactivated fairground pack'}'


@directFunction
def setTokens():
    userData = loadSave()
    amount = promptInt('Set revive token amount: ')
    userData['Global']['ReviveTokens'] = amount
    writeSave(userData)
    return f"Set revive tokens to {amount}"


@directFunction
def removeAds():
    userData = loadSave()
    userData['Global']['ForceRemoveAds'] = not userData['Global']['ForceRemoveAds']
    writeSave(userData)
    return f'{'Removed ads' if userData['Global']['ForceRemoveAds'] else 'Ads have been turned on'}'


@directFunction
def setNightmareTickets():
    userData = loadSave()
    amount = promptInt('Set nightmare tickets amount: ')
    userData['Global']['AvailablePremiumTickets'] = amount
    writeSave(userData)
    return f"Set nightmare tickets to {amount}"


@nestedMenuOptions
def unlockWeaponCollection(weaponType: str = '__menu_options__'):
    items = loadItems()
    
    if weaponType == '__menu_options__':
        return {w.capitalize().replace('_', ' '): unlockWeaponCollection for w in items['weapons'].keys()}
    
    def setWeaponVersion(version: str = '__menu_options__'):
        if version == '__menu_options__':
            return {v.capitalize(): setWeaponVersion for v in items['weapons'][weaponType.lower().replace(' ', '_')].keys()}
        
        WEAPONS = items['weapons'][weaponType.lower().replace(' ', '_')][version.lower()]
        
        def unlockWeapon(weapon: str = '__menu_options__'):
            if weapon == '__menu_options__':
                return {w['Name']: unlockWeapon for w in WEAPONS}
            
            selectedWeapon = next((w for w in WEAPONS if w['Name'] == weapon), None)
            if selectedWeapon:
                userData = loadSave()
                weaponID = selectedWeapon['ID']
                
                for x in userData['CollectionArrayWeapon']:
                    if x['CollectionId'] == weaponID:
                        x['CollectionUnlocked'] = not x['CollectionUnlocked']
                        writeSave(userData)
                        return f'{weapon} ({version}) has been {'unlocked' if x['CollectionUnlocked'] else 'locked'} in the collection.'
                
                return f'Could not find {weapon} ({version}) in the collection.'
        
        return unlockWeapon()
    
    return setWeaponVersion()


@nestedMenuOptions
def unlockArmorCollection(armorType: str = '__menu_options__'):
    items = loadItems()
    
    if armorType == '__menu_options__':
        return {a.capitalize().replace('_', ' '): unlockArmorCollection for a in items['armour'].keys()}
    
    def setArmorVersion(version: str = '__menu_options__'):
        if version == '__menu_options__':
            return {v.capitalize(): setArmorVersion for v in items['armour'][armorType.lower().replace(' ', '_')].keys()}
        
        ARMORS = items['armour'][armorType.lower().replace(' ', '_')][version.lower()]
        
        def unlockArmor(armor: str = '__menu_options__'):
            if armor == '__menu_options__':
                return {a['Name']: unlockArmor for a in ARMORS}
            
            selectedArmor = next((a for a in ARMORS if a['Name'] == armor), None)
            if selectedArmor:
                userData = loadSave()
                armorID = selectedArmor['ID']
                
                for x in userData['CollectionArrayArmour']:
                    if x['CollectionId'] == armorID:
                        x['CollectionUnlocked'] = not x['CollectionUnlocked']
                        writeSave(userData)
                        return f'{armor} ({version}) has been {'unlocked' if x['CollectionUnlocked'] else 'locked'} in the collection.'
                
                return f'Could not find {armor} ({version}) in the collection.'
        
        return unlockArmor()
    
    return setArmorVersion()


@nestedMenuOptions
def toggleCollectionRewards(category: str = '__menu_options__'):
    userData = loadSave()
    rewards = userData['CollectionRewards']

    weaponRewards = [key for key in rewards.keys() if key.startswith('CollectionRewardWeapon') or 
                      any(weapon in key for weapon in ['Pistol', 'SMG', 'Assault', 'Shotgun', 'Sniper', 'Rocket', 'LMG'])]
    armourRewards = [key for key in rewards.keys() if key.startswith('CollectionRewardArmour') or 
                     any(armor in key for armor in ['Helmet', 'Torso', 'Gloves', 'Pants', 'Boots'])]

    def toggleReward(reward: str = '__menu_options__'):
        if reward == '__menu_options__':
            return {key: toggleReward for key in rewards.keys() if key in (weaponRewards if category == 'Weapons' else armourRewards)}
        
        if reward == 'Toggle All':
            new_value = not all(rewards[key] for key in (weaponRewards if category == 'Weapons' else armourRewards))
            for key in (weaponRewards if category == 'Weapons' else armourRewards):
                rewards[key] = new_value
            writeSave(userData)
            return f"All {category} rewards set to {new_value}"
        
        rewards[reward] = not rewards[reward]
        writeSave(userData)
        return f"{reward} set to {rewards[reward]}"

    if category == '__menu_options__':
        return {
            'Weapons': toggleCollectionRewards,
            'Armor': toggleCollectionRewards
        }

    options = toggleReward()
    options['Toggle All'] = toggleReward
    return options


ACCOUNT = {
    'Factions': {
        'Set credits': setCredits,
        'Change guild': changeGuild
    },
    'IAP Settings': {
        'Unlock profiles': unlockProfiles,
        'Unlock fairground pack': unlockFairground
    },
    'Remove ads (Mobile only)': removeAds,
    'Revive tokens': setTokens,
    'Nightmare tickets': setNightmareTickets,
    'Unlock collections': {
        'Weapon collection': unlockWeaponCollection,
        'Armour collection': unlockArmorCollection
    },
    'Toggle rewards': toggleCollectionRewards
}