from pathlib import Path
from win32api import RegOpenKeyEx, RegQueryValueEx
from win32con import HKEY_CURRENT_USER
from os import environ, system, name
from vdf import parse as vdfparse
from typing import Union, Optional, Iterator, Literal, Callable, List, Dict, Any
from json import loads as jsloads, load as jsload, dump as jsdump, dumps as jsdumps, JSONDecodeError
from dataclasses import dataclass
from msvcrt import getch
from steamid_converter.Converter import to_steamID3
from lib.gameio import iterDecodeFromFile, encodeToFile
from inspect import signature
from functools import wraps
from tkinter import Tk, filedialog
from base64 import b64decode
from zlib import decompress as zdecompress


@dataclass
class const:
    CWD: Path = Path.cwd()
    CONFIG_PATH: Path = CWD / 'config.json'
    ITEMS_PATH: Path = CWD / 'items.json'
    DEFAULT_CONFIG = {'steam_id': None,'current_profile': None,'active_profiles': None}
    VERSION: str = '4.0.0'
    ITEMS: str = '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'


@dataclass
class F:
    RESET: str = '\u001B[0m'
    RED: str = '\u001B[31m'
    GREEN: str = '\u001B[32m'
    YELLOW: str = '\u001B[33m'
    CYAN: str = '\u001B[36m'
    WHITE: str = '\u001B[37m'


def selectFileWindow(title: str = "Select a file", filetypes: list = None) -> Path:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    filePath = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return Path(filePath) if filePath else None


def getSteamPath() -> Optional[Path]:
    """
    Return the Steam installation path,
    """
    steamEnv = environ.get('STEAM_PATH')
    if steamEnv:
        return Path(steamEnv).resolve(strict=True)

    regDirPath = RegOpenKeyEx(HKEY_CURRENT_USER, r'Software\Valve\Steam')
    regValue = RegQueryValueEx( regDirPath, 'SteamPath' )
    return Path(regValue[0]).resolve(strict=True)


def iterGameSavePaths() -> Iterator[Path]:
    cls()
    config = loadConfig()
    steamID = config.get('steam_id')
    if not steamID:
        raise ValueError("Steam ID is not set in the config file.")
    
    try:
        userId = to_steamID3(str(steamID)).strip("[]").split(":", 2)[-1]
    except ValueError as e:
        raise ValueError(f"Invalid Steam ID in config: {steamID}. Error: {str(e)}")

    try:
        profilePath = Path(
            getSteamPath()
            / 'userdata'
            / userId
            / '678800'
            / 'local/Data/Docs/'
        ).resolve(strict=True)
    except Exception as e:
        print(f'Error finding game save path: {str(e)}')
        print(f'User ID: {userId}\nSteam ID: {steamID}')
        raise ValueError("Unable to locate game save path.") from e

    for folder in profilePath.iterdir():
        if not folder.is_dir() or len(folder.name) < 24:
            continue
        
        savePath = folder / 'Profile.save'
        if savePath.exists():
            yield savePath

    mainSavePath = profilePath / 'Profile.save'
    if mainSavePath.exists():
        yield mainSavePath


def getProfileSavePath():
    try:
        return next( iterGameSavePaths() )
    except StopIteration:
        return None


def getSteamLibraryPath() -> Optional[Path]:
    """
    Return the Steam library path that has the SAS:ZA4 game installed.
    """
    steamPath = getSteamPath()
    libraryFoldersFile = steamPath / 'steamapps' / 'libraryfolders.vdf'

    SASZASteamAppID = '678800'

    try:
        with libraryFoldersFile.open('r') as f:
            libraryFolders = vdfparse(f)['libraryfolders']

        for folder in libraryFolders.values():
            if not isinstance(folder, dict):
                continue

            installedApps = folder.get('apps')
            if not isinstance(installedApps, dict):
                continue

            if SASZASteamAppID in installedApps:
                return Path(folder['path']).resolve(strict=True)

    except (FileNotFoundError, KeyError):
        pass

    return None


def iterSteamLoggedUsers( ):
    """
    Yields generator object containing steam username and steam id
    """
    steamPath = getSteamPath()
    loginUsersFile = steamPath / 'config' / 'loginusers.vdf'
    try:
        with loginUsersFile.open('r') as f:
            usersData = vdfparse(f).get('users', {})
            for steamId, userData in usersData.items():
                accountName = userData.get('AccountName', '')
                if accountName:
                    yield accountName, steamId
    except (FileNotFoundError, KeyError):
        pass

    return None


def isGameInstalled() -> bool:
    steamPath = getSteamPath()
    gamePath = steamPath / 'steamapps' / 'common' / 'SAS Zombie Assault 4'
    try:
        return Path(gamePath).resolve(strict=True).exists()
    except:
        raise 'Game is not installed!'

def promptInt(prompt: str, minValue: Optional[int] = None, maxValue: Optional[int] = None) -> int:
    """
    Prompt the user for an integer input within an optional range.

    :param prompt: The prompt message to display to the user.
    :param minValue: The minimum acceptable value (inclusive), if any.
    :param maxValue: The maximum acceptable value (inclusive), if any.
    :return: The validated integer input from the user.
    """
    message = None
    while True:
        printTitle(message)
        try:
            userInput = int(input(prompt))
            if minValue is not None and userInput < minValue:
                message = f"{F.RED}Please enter a number greater than or equal to {minValue}.{F.WHITE}"
            elif maxValue is not None and userInput > maxValue:
                message = f"{F.RED}Please enter a number less than or equal to {maxValue}.{F.WHITE}"
            else:
                return userInput
        except ValueError:
            message = f"{F.RED}Invalid input. Please enter a valid integer.{F.WHITE}"


def promptChoice(options: List[Union[str, tuple, list]], prompt: Optional[str] = None) -> Union[str, tuple, list]:
    printTitle()
    if prompt:
        print(prompt)
    for i, option in enumerate(options):
        if i < 9:
            key = str(i + 1)
        else:
            key = chr(ord('A') + i - 9)
        if isinstance(option, (tuple, list)):
            print(f"[{key}] {' - '.join(map(str, option))}")
        else:
            print(f"[{key}] {option}")
    print('\n[ > ] ', end='', flush=True)

    validKeys = {str(i + 1): i for i in range(min(9, len(options)))}
    validKeys.update({chr(ord('A') + i - 9): i for i in range(9, len(options))})

    while True:
        key = getch().decode('ascii').upper()
        if key in validKeys:
            return options[validKeys[key]]


def promptStr(prompt: str, options: Optional[List[str]] = None, caseSensitive: bool = False) -> str:
    """
    Prompt the user for a string input, optionally matching against a list of allowed options.

    :param prompt: The prompt message to display to the user.
    :param options: A list of allowed string options, if any.
    :param caseSensitive: Whether the matching should be case-sensitive.
    :return: The validated string input from the user.
    """
    
    while True:
        printTitle()
        userInput = input(prompt)
        
        if options is None:
            return userInput
        
        if not caseSensitive:
            userInput = userInput.lower()
            options = [opt.lower() for opt in options]
        
        if userInput in options:
            return options[options.index(userInput)]
        else:
            print(f"Invalid input. Please choose from: {', '.join(options)}")


def promptYN(prompt: str) -> bool:
    """
    Prompt the user for a yes/no response.

    :param prompt: The prompt message to display to the user.
    :return: True for 'yes', False for 'no'.
    """
    
    while True:
        printTitle()
        userInput = input(f"{prompt} (y/n): ").lower()
        if userInput in ['y', 'yes']:
            return True
        elif userInput in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def loadSave() -> Any:
    try:
        rawData = b''.join(iterDecodeFromFile(getProfileSavePath()))
        data = jsloads(rawData)
        if not isinstance(data, dict) or 'Inventory' not in data or not isinstance(data['Inventory'], dict):
            raise ValueError("Unexpected save file structure")
        return data
    except JSONDecodeError as e:
        print(f"Error decoding save file: {e}")
        return None
    except Exception as e:
        print(f"Error loading save file: {e}")
        return None


def writeSave(data: str) -> None:
    return encodeToFile(jsdumps(data).encode("utf-8"), getProfileSavePath().open("wb+"))


def getProfiles() -> List[str]:
    data = loadSave()
    if data is None:
        return []
    try:
        return [i for i in data['Inventory'].keys() if isinstance(data['Inventory'][i], dict) and data['Inventory'][i].get('Loaded')]
    except Exception as e:
        print(f"Error parsing profiles: {e}")
        return []


def checkGameInstallation() -> None:
    if not isGameInstalled():
        raise RuntimeError('Game is not installed!')
    return True


def createConfigFileIfMissing() -> None:
    if not const.CONFIG_PATH.exists():
        print('Creating missing config file...')
        const.CONFIG_PATH.touch()
        writeDefaultConfig()

    if const.CONFIG_PATH.stat().st_size == 0:
        writeDefaultConfig()


def writeDefaultConfig() -> None:
    with open(const.CONFIG_PATH, 'w') as f:
        jsdump(const.DEFAULT_CONFIG, f, indent=4)


def validateConfigKeys(data: Dict[str, Any]) -> None:
    if list(data.keys()) != list(const.DEFAULT_CONFIG.keys()):
        print('Fixing invalid config file...')
        writeDefaultConfig()


def updateSteamIDIfMissing(data: Dict[str, Any]) -> None:
    if not data.get('steam_id'):
        print('SteamID not found in config file!')
        steamUsers = list(iterSteamLoggedUsers())
        if not steamUsers:
            raise ValueError("No logged-in Steam users found.")
        selected = promptChoice(options=steamUsers, prompt='Select your SteamID:')
        if selected:
            data['steam_id'] = int(selected[1])
            writeConfig(data)
        else:
            raise ValueError("No SteamID selected.")
    return data['steam_id']



def updateProfileInfoIfMissing(data: Dict[str, Any]) -> None:
    profiles = getProfiles()
    if not profiles:
        print("Warning: No profiles found in the save file.")
        return
    
    if not data.get('current_profile') or data['current_profile'] not in profiles:
        data['current_profile'] = promptChoice(options=profiles, prompt='Select your current profile:')
    
    data['active_profiles'] = profiles
    writeConfig(data)


def loadItems():
    with open(const.ITEMS_PATH) as f:
        return jsload(f)


def writeConfig(data: Dict[str, Any]) -> None:
    with open(const.CONFIG_PATH, 'w') as f:
        jsdump(data, f, indent=4)


def loadConfig() -> Dict[str, Any]:
    try:
        with open(const.CONFIG_PATH) as f:
            return jsload(f)
    except JSONDecodeError:
        print("Error: Config file is corrupted. Creating a new one.")
        writeDefaultConfig()
        return const.DEFAULT_CONFIG
    except FileNotFoundError:
        print("Error: Config file not found. Creating a new one.")
        writeDefaultConfig()
        return const.DEFAULT_CONFIG


def initCheck():
    try:
        checkGameInstallation()
        if not const.ITEMS_PATH.exists():
            const.ITEMS_PATH.touch()
            decoded = b64decode(const.ITEMS)
            decompressed = jsloads(zdecompress(decoded))
            with open(const.ITEMS_PATH, 'w') as f:
                jsdump(decompressed, f)

        createConfigFileIfMissing()
        data = loadConfig()
        validateConfigKeys(data)
        updateSteamIDIfMissing(data)
        updateProfileInfoIfMissing(data)
        
        if not data.get('steam_id') or not data.get('current_profile') or not data.get('active_profiles'):
            print("Warning: Some required fields are still missing in the config.")
            print(f"Current config: {data}")
        
        writeConfig(data)
    except Exception as e:
        print(f"Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        exit()


def cls():
    system('cls' if name == 'nt' else 'clear')


def printTitle(extra: Optional[str] = None):
    if extra == '':
        extra = None
    cls()
    config = loadConfig()
    part1 = r'''
           _______   __________________  ____  __ 
          / __/ _ | / __/ / /_  __/ __ \/ __ \/ / 
         _\ \/ __ |_\ \/_  _// / / /_/ / /_/ / /__
        /___/_/ |_/___/ /_/ /_/  \____/\____/____/'''
    part2 = f'''
{F.RED}{part1}{F.WHITE}
\t\t{F.CYAN}made by: 0dx | ver: {const.VERSION}{F.WHITE}

{F.WHITE}Selected Profile: [{F.GREEN}{config['current_profile']}{F.WHITE}]
'''
    if extra:
        part2 += f'\n{extra}\n'
    
    print(part2)


def getFuncInputs(func: Callable) -> Dict[str, Any]:
    params = signature(func).parameters
    inputs = {}
    for name, param in params.items():
        if param.annotation == int:
            inputs[name] = promptInt(f"Enter {name}: ")
        elif param.annotation == str:
            inputs[name] = promptStr(f"Enter {name}: ")
        elif param.annotation == List[str]:
            inputs[name] = promptChoice(param.default, f"Select {name}:")
        else:
            inputs[name] = promptStr(f"Enter {name} ({param.annotation.__name__}): ")
    return inputs


def handleMenu(menu: Dict[str, Any], title: str = "Main Menu", parent: Optional[Dict[str, Any]] = None, message: Optional[str] = None) -> None:
    while True:
        printTitle(message)
        print(f"{F.YELLOW}{title}{F.WHITE}\n")
        
        options = list(menu.keys())
        for i, option in enumerate(options):
            if i < 9:
                print(f"[{i+1}] {option}")
            else:
                print(f"[{chr(ord('A') + i - 9)}] {option}")
        
        print("\nPress [ESC] to go back/exit")
        print('\n[ > ] ', end='', flush=True)
        
        key = getch()
        
        if key == b'\x1b':
            if parent:
                return
            else:
                cls()
                print("\nExiting...")
                exit()
        
        if key in (b'\xe0', b'\x00'):
            key = getch()
            continue
        
        try:
            key = key.decode('ascii').upper()
        except UnicodeDecodeError:
            continue
        
        index = -1
        
        if key.isdigit() and 1 <= int(key) <= min(9, len(options)):
            index = int(key) - 1
        elif 'A' <= key <= 'Z':
            index = ord(key) - ord('A') + 9
        
        if 0 <= index < len(options):
            selectedOption = options[index]
            value = menu[selectedOption]
            
            if callable(value):
                if getattr(value, '__direct_function__', False):
                    result = value()
                    message = f"{F.GREEN}Function call: {result}{F.RESET}" if result else f"{F.YELLOW}Function executed with no return value.{F.RESET}"
                elif hasattr(value, '__menu_options__'):
                    menuOptions = value.__menu_options__()
                    if isinstance(menuOptions, list):
                        new_menu = {option: lambda o=option: value(o) for option in menuOptions}
                        handleMenu(new_menu, title=selectedOption, parent=menu)
                    else:
                        message = f"{F.RED}Error: Menu options must be a list{F.RESET}"
                else:
                    result = value()
                    message = f"{F.GREEN}Function call: {result}{F.RESET}" if result else f"{F.YELLOW}Function executed with no return value.{F.RESET}"
            elif isinstance(value, dict):
                handleMenu(value, title=selectedOption, parent=menu)
            else:
                message = f"{F.CYAN}Selected: {selectedOption}{F.RESET}"
        else:
            message = f"{F.RED}Error: Option does not exist!{F.RESET}"


def directFunction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__direct_function__ = True
    return wrapper


def menuOptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__menu_options__ = func
    return wrapper


def nestedMenuOptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def navigateMenus(initialMenu):
            menuStack = [initialMenu]
            pathStack = []
            message = None

            while menuStack:
                currentMenu = menuStack[-1]
                currentPath = ' > '.join(pathStack)

                printTitle(message)
                print(f"{F.YELLOW}Current menu: {currentPath}{F.WHITE}\n")

                options = list(currentMenu.keys())
                for i, option in enumerate(options):
                    key = str(i + 1) if i < 9 else chr(ord('A') + i - 9)
                    print(f"[{key}] {option}")

                print("\nPress [ESC] to go back/exit")
                print('\n[ > ] ', end='', flush=True)

                key = getch()
                
                if key == b'\x1b':
                    if len(menuStack) == 1:
                        return
                    menuStack.pop()
                    pathStack.pop()
                    message = None
                    continue

                if key in (b'\xe0', b'\x00'):
                    getch()
                    continue

                try:
                    userInput = key.decode('ascii').upper()
                except UnicodeDecodeError:
                    continue

                selectedIndex = -1
                if userInput.isdigit() and 1 <= int(userInput) <= min(9, len(options)):
                    selectedIndex = int(userInput) - 1
                elif 'A' <= userInput <= 'Z':
                    selectedIndex = ord(userInput) - ord('A') + 9

                if 0 <= selectedIndex < len(options):
                    selectedOption = options[selectedIndex]
                    value = currentMenu[selectedOption]

                    if callable(value):
                        result = value(selectedOption)
                        if isinstance(result, dict):
                            menuStack.append(result)
                            pathStack.append(selectedOption)
                            message = None
                        elif result is not None:
                            message = f"{F.GREEN}Function call: {result}{F.RESET}"
                    elif isinstance(value, dict):
                        menuStack.append(value)
                        pathStack.append(selectedOption)
                        message = None
                else:
                    message = f"{F.RED}Invalid option. Please try again.{F.RESET}"

        result = func(*args, **kwargs)
        if isinstance(result, dict):
            navigateMenus(result)
            return None
        return result

    return wrapper