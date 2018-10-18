"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings
from pyfiglet import figlet_format
from uploader.helpers import get_quiz_files




class QuestionCreator(object):
    intro_message_color = "yellow"

    def __init__(self, question_folder, creator_name):
        self.question_folder = question_folder
        self.creator_name = creator_name
        self.prompt_session = PromptSession()
        self.bindings = KeyBindings()

        @self.bindings.add('c-q')  # This just makes the program exit nice when the user holds down control and Q
        def _(event):
            event.app.exit()

    def run(self):
        self.print_intro_message()
        quiz_id = self.request_quiz_id()

    def print_intro_message(self):
        print(figlet_format(self.creator_name))
        print("Press Control + Q at any time to quit")
        print("\n\n")  # Print some new lines

    def request_quiz_id(self):
        available_quizzes_list = get_quiz_files(self.question_folder)  # First get the applicable quiz files
        striped_available_quizzes_list = [s[:s.rindex(".")] for s in available_quizzes_list]  # Then strip the endings
        available_quizzes_string = ", ".join(
            striped_available_quizzes_list)  # Join them to print which ones are available

        print(f"Available Quizzes: {available_quizzes_string}")
        quiz_id_completer = WordCompleter(striped_available_quizzes_list)
        quiz_id_validator = QuizIdValidator(striped_available_quizzes_list)
        quiz_id = self.prompt_session.prompt("What quiz would you like to add a question to? ",
                                             completer=quiz_id_completer, validator=quiz_id_validator,
                                             validate_while_typing=True, key_bindings=self.bindings)
        return quiz_id


class QuizIdValidator(Validator):
    def __init__(self, quiz_id_list):
        self.quiz_id_list = quiz_id_list

    def validate(self, document):
        if document.text not in self.quiz_id_list:
            raise ValidationError(message="Sorry that is not a valid quiz.")
