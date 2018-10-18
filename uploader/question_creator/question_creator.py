"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

import sys

from prompt_toolkit import prompt
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from uploader.helpers import get_quiz_files
from uploader import QUESTION_FOLDER

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


class QuestionCreator(object):
    creator_name = "Question_Creator"
    intro_message_color = "yellow"

    def run(self):
        self.print_intro_message()
        print(get_quiz_files(QUESTION_FOLDER))
        quiz_id = prompt("What quiz would you like to add a question to? ")
        print("You said: %s" % quiz_id)

    def print_intro_message(self):
        cprint(figlet_format(self.creator_name, ), self.intro_message_color, attrs=['bold'])
