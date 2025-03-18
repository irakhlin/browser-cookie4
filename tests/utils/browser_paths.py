import os
import sys

from . import BrowserName, logger


def get_username():
    try:
        return os.getlogin()
    except OSError:
        return os.environ.get('USERNAME') or os.environ.get('USER') or ''


BIN_LOCATIONS = {
    BrowserName.CHROME: {
        'linux': ['/usr/bin/google-chrome-stable'],
        'windows': [
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        ],
        # Not tested
        'macos': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    },
    BrowserName.CHROMIUM: {
        'linux': ['/usr/bin/chromium', '/usr/bin/chromium-browser'],
        'windows': [
            r'C:\Program Files (x86)\Chromium\Application\chrome.exe',
            r'C:\Program Files\Chromium\Application\chrome.exe'
        ],
        # Not tested
        'macos': ['/Applications/Chromium.app/Contents/MacOS/Chromium']
    },
    BrowserName.BRAVE: {
        'linux': ['/usr/bin/brave', '/usr/bin/brave-browser'],
        'windows': [
            r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe',
            r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
            fr'C:\Users\{get_username()}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe'
        ],
        # Not tested
        'macos': ['/Applications/Brave Browser.app/Contents/MacOS/Brave Browser']
    },
    BrowserName.EDGE: {
        'linux': ['/usr/bin/microsoft-edge-stable'],
        'windows': [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
        ],
        # Not tested
        'macos': ['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']
    },
    BrowserName.FIREFOX: {
        'linux': ['/usr/bin/firefox'],
        'windows': [
            r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
            r'C:\Program Files\Mozilla Firefox\firefox.exe'
        ],
        # Not tested
        'macos': ['/Applications/Firefox.app/Contents/MacOS/firefox']
    },
    BrowserName.LIBREWOLF: {
        'linux': ['/usr/bin/librewolf'],
        'windows': [
            r'C:\Program Files (x86)\LibreWolf\librewolf.exe',
            r'C:\Program Files\LibreWolf\librewolf.exe',
            fr'C:\Users\{get_username()}\AppData\Local\LibreWolf\librewolf.exe'
        ],
        # Not tested
        'macos': ['/Applications/LibreWolf.app/Contents/MacOS/LibreWolf']
    },
    BrowserName.OPERA: {
        'linux': ['/usr/bin/opera'],
        'windows': [
            r'C:\Program Files (x86)\Opera\opera.exe',
            r'C:\Program Files\Opera\opera.exe',
            fr'C:\Users\{get_username()}\AppData\Local\Programs\Opera\opera.exe'
        ],
        'macos': ['/Applications/Opera.app/Contents/MacOS/Opera']  # Not tested
    },
    BrowserName.OPERA_GX: {
        'linux': [],
        'windows': [
            r'C:\Program Files (x86)\Opera GX\opera.exe',
            r'C:\Program Files\Opera GX\opera.exe',
            fr'C:\Users\{get_username()}\AppData\Local\Programs\Opera GX\opera.exe'
        ],
        # Not tested
        'macos': ['/Applications/Opera GX.app/Contents/MacOS/Opera GX']
    },
    BrowserName.VIVALDI: {
        'linux': ['/usr/bin/vivaldi-stable'],
        'windows': [
            r'C:\Program Files (x86)\Vivaldi\Application\vivaldi.exe',
            r'C:\Program Files\Vivaldi\Application\vivaldi.exe',
            fr'C:\Users\{get_username()}\AppData\Local\Vivaldi\Application\vivaldi.exe'
        ],
        # Not tested
        'macos': ['/Applications/Vivaldi.app/Contents/MacOS/Vivaldi']
    }
}


class BinaryLocation:
    def __init__(self, raise_not_found=False):
        self.__raise_not_found = raise_not_found
        if sys.platform == 'darwin':
            self.__os = 'macos'
        elif sys.platform.startswith('linux') or 'bsd' in sys.platform.lower():
            self.__os = 'linux'
        elif sys.platform == "win32":
            self.__os = 'windows'
        else:
            raise ValueError('unsupported os')

    def get(self, browser: str) -> str:
        for i in BIN_LOCATIONS[browser][self.__os]:
            if os.path.exists(i):
                logger.info(f'found {browser} binary at: {i}')
                return i
        if self.__raise_not_found:
            raise FileNotFoundError('browser not found')
        logger.warning(f'could not find {browser} binary')
