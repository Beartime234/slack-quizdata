"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

import sys

from prompt_toolkit import prompt
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


def create():
    cprint(figlet_format('Slack-Quizdata',),'yellow', attrs=['bold'])
    # answer = prompt('Give me some input: ')
    # print('You said: %s' % answer)


if __name__ == '__main__':
    create()
