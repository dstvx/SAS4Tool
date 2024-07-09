from lib.utilities import (
    getProfileSavePath,
    directFunction,
    menuOptions,
    loadConfig,
    writeConfig,
    const,
    loadSave,
    jsdump,
    JSONDecodeError,
    jsload,
    writeSave,
    selectFileWindow,
    getProfiles
)

from shutil import copy2
from datetime import datetime


@menuOptions
def changeCurrentProfile(profile: str = "__menu_options__"):
    config = loadConfig()
    activeProfiles = config.get('active_profiles', [])
    
    if profile == "__menu_options__":
        return activeProfiles
    try:
        if profile not in activeProfiles:
            return f"Invalid profile: {profile}"
    except Exception as e:
        return f'Error: {e}'
    
    config['current_profile'] = profile
    writeConfig(config)
    return f"Changed current profile to {profile}"


@directFunction
def backUpSaveFile():
    saveFile = getProfileSavePath()
    if not saveFile:
        return "Error: Could not find save file."

    backupDir = const.CWD / 'backups' / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backupDir.mkdir(parents=True, exist_ok=True)

    outPath = backupDir / saveFile.name
    copy2(saveFile, outPath)

    return f'Backed up Profile.save to {outPath}'


@directFunction
def exportSaveAsJson():
    saveData = loadSave()
    if not saveData:
        return "Error: Could not load save data."

    exportDir = const.CWD / 'exports' / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    exportDir.mkdir(parents=True, exist_ok=True)

    outPath = exportDir / 'Profile.json'
    with open(outPath, 'w') as f:
        jsdump(saveData, f, indent=4)

    return f'Exported save data as JSON to {outPath}'


@directFunction
def importJsonAsProfile():
    jsonPath = selectFileWindow("Select JSON file to import", [("JSON files", "*.json")])
    if not jsonPath:
        return "Import cancelled."

    try:
        with open(jsonPath, 'r') as f:
            jsonData = jsload(f)
    except JSONDecodeError:
        return f"Error: {jsonPath} is not a valid JSON file."
    except IOError:
        return f"Error: Could not read file {jsonPath}."

    try:
        writeSave(jsonData)
    except Exception as e:
        return f"Error writing save file: {str(e)}"

    return f"Successfully imported {jsonPath} as the new profile."


@directFunction
def replaceProfileSave():
    savePath = selectFileWindow("Select .save file to import", [("Save files", "*.save")])
    if not savePath:
        return "Import cancelled."
    currentSave = getProfileSavePath()
    if not currentSave:
        return "Error: Could not find current save file location."

    try:
        copy2(savePath, currentSave)
    except IOError as e:
        return f"Error copying file: {str(e)}"

    return f"Successfully replaced profile with {savePath}."


@directFunction
def updateActiveProfiles():
    config = loadConfig()
    currentProfiles = getProfiles()
    config['active_profiles'] = currentProfiles
    writeConfig(config)
    return f"Active profiles updated. Current profiles: {', '.join(currentProfiles)}"


CFG = {
    'Change selected profile': changeCurrentProfile,
    'Back up Profile.save': backUpSaveFile,
    'Export .SAVE as .JSON': exportSaveAsJson,
    'Import .JSON as .SAVE': importJsonAsProfile,
    'Replace .SAVE with .SAVE': replaceProfileSave,
    'Update active profiles': updateActiveProfiles
}