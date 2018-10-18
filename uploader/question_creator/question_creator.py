"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

import sys

from prompt_toolkit import PromptSession
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from uploader.helpers import get_quiz_files
from uploader import QUESTION_FOLDER

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


class QuestionCreator(object):
    creator_name = "Slack Question Creator"
    intro_message_color = "yellow"

    def run(self):
        self.print_intro_message()
        available_quizzes = get_quiz_files(QUESTION_FOLDER)
        prompt_session = PromptSession()
        print(f"Available Quizzes {available_quizzes}")
        quiz_id = prompt_session.prompt("What quiz would you like to add a question to? ")
        print("You said: %s" % quiz_id)

    def print_intro_message(self):
        cprint(figlet_format(self.creator_name, ), self.intro_message_color, attrs=['bold'])
