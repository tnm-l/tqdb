"""
Utility module to prepare the data for the parser.

"""
import logging
import subprocess
import winreg

from pathlib import Path


# Titan Quest Anniversary Edition registry key:
LOOKUP_KEY = (r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
              r'\Steam App 475150')

# Extract commands to run:
COMMANDS = [
    ['Toolset/Templates.arc', 'data/database'],
    ['Text/Text_CH.arc', 'data/resources/zh'],
    ['Text/Text_CZ.arc', 'data/resources/cs'],
    ['Text/Text_DE.arc', 'data/resources/de'],
    ['Text/Text_EN.arc', 'data/resources/en'],
    ['Text/Text_ES.arc', 'data/resources/es'],
    ['Text/Text_FR.arc', 'data/resources/fr'],
    ['Text/Text_IT.arc', 'data/resources/it'],
    ['Text/Text_JA.arc', 'data/resources/ja'],
    ['Text/Text_KO.arc', 'data/resources/ko'],
    ['Text/Text_PL.arc', 'data/resources/pl'],
    ['Text/Text_RU.arc', 'data/resources/ru'],
    ['Text/Text_UK.arc', 'data/resources/uk'],
    ['Resources/Quests.arc', 'data/quests'],
    ['Resources/XPack/Quests.arc', 'data/quests'],
    ['Resources/XPack2/Quests.arc', 'data/quests'],
    ['Resources/XPack3/Quests.arc', 'data/quests'],
    ['Resources/XPack4/Quests.arc', 'data/quests'],
    ['Resources/Items.arc', 'data/textures/Items'],
    ['Resources/XPack/Items.arc', 'data/textures/XPack/Items'],
    ['Resources/XPack2/Items.arc', 'data/textures/XPack2/Items'],
    ['Resources/XPack3/Items.arc', 'data/textures/XPack3/Items'],
    ['Resources/XPack4/Item.arc', 'data/textures/XPack4/Item'],
]

# Required directories for this parser:
DIRECTORIES = [
    'data/database',
    'data/quests',
    'data/resources/cs',
    'data/resources/de',
    'data/resources/en',
    'data/resources/es',
    'data/resources/fr',
    'data/resources/it',
    'data/resources/ja',
    'data/resources/ko',
    'data/resources/pl',
    'data/resources/ru',
    'data/resources/uk',
    'data/resources/zh',
    'data/textures/xpack4/Item',
    'data/textures/xpack3/Items',
    'data/textures/XPack2/Items',
    'data/textures/XPack/Items',
    'data/textures/Items',
]


def tqdb_prepare():
    # Open the TQAE key and grab the install location:
    try:
        tqae_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, LOOKUP_KEY, 0, winreg.KEY_READ)
    except FileNotFoundError:
        import platform

        bitness = platform.architecture()[0]
        if bitness == '32bit':
            other_view_flag = winreg.KEY_WOW64_64KEY
        elif bitness == '64bit':
            other_view_flag = winreg.KEY_WOW64_32KEY
        else:
            raise RuntimeError("Platform architecture not recognized: " +
                               bitness)

        try:
            tqae_key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, LOOKUP_KEY,
                access = winreg.KEY_READ | other_view_flag)
        except WindowsError as err:
            raise RuntimeError('Could not find installation directory for '
                               'Titan Quest.') from err

    try:
        install = winreg.QueryValueEx(tqae_key, 'InstallLocation')[0]
    except WindowsError as err:
        raise RuntimeError('Could not find installation directory for Titan '
                           'Quest.') from err

    logging.info("Found TQ installation directory: " + install)

    # Create the required directories if necessary
    for d in DIRECTORIES:
        Path(d).mkdir(parents=True, exist_ok=True)

    # Run the extraction commands:
    tool = Path(install, 'ArchiveTool.exe')
    for c in COMMANDS:
        input_file = Path(install, c[0])
        subprocess.run([
            # ArchiveTool.exe in the TQ Install directory
            str(tool),
            # Resource ARC file in the TQ Install directory
            str(input_file),
            # Extract flag for the ArchiveTool executable
            '-extract',
            # Output directory (local data/ dir)
            str(Path(c[1]).absolute()),
        ])


if __name__ == '__main__':
    tqdb_prepare()
