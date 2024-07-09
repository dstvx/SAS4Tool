#!/usr/bin/env python3
from lib.utilities import initCheck, handleMenu
from lib.account import ACCOUNT
from lib.cfg import CFG
from lib.profile import PROFILE
from sys import exit


MAIN = {
    'Account': ACCOUNT,
    'Profile': PROFILE,
    'Config': CFG
}


def main():
    handleMenu(MAIN)


if __name__ == '__main__':
    initCheck()
    main()
    exit()
