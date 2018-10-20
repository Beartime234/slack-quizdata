"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator, ValidationError
from pyfiglet import figlet_format

from uploader.helpers import get_quiz_files, generate_unique_id, save_question_to_question_file


class QuestionCreator(object):
    intro_message_color = "yellow"

    def __init__(self, question_folder: str, creator_name: str = "Question Creator"):
        """Initializer for Question Creator Obj

        Args:
            question_folder: The folder which the question yaml lives in
            creator_name: The name of the question creator
        """
        self.question_folder = question_folder
        self.creator_name = creator_name
        self.quiz_id_prompt_session = PromptSession()
        self.question_prompt_session = PromptSession()
        self.bindings = KeyBindings()

        @self.bindings.add('c-q')  # This just makes the program exit nice when the user holds down control and Q
        def _(event):
            event.app.exit()

    def run(self):
        """Runs the app
        """
        self.print_intro_message()
        quiz_id = self.request_quiz_id()
        question_file = self.get_quiz_file(quiz_id)
        question = self.ask_for_question()
        print("Saving Question...")
        save_question_to_question_file(question, f"{self.question_folder}{question_file}")

    def print_intro_message(self):
        """Prints the introduction message
        """
        print(figlet_format(self.creator_name))
        print("Press Control + Q at any time to quit")
        print("\n\n")  # Print some new lines

    def request_quiz_id(self):
        """Runs the prompts for getting the quiz id the user wishes to work with=
        """
        available_quizzes_list = get_quiz_files(self.question_folder)  # First get the applicable quiz files
        striped_available_quizzes_list = [s[:s.rindex(".")] for s in available_quizzes_list]  # Then strip the endings
        available_quizzes_string = ", ".join(
            striped_available_quizzes_list)  # Join them to print which ones are available

        print(f"Available Quizzes: {available_quizzes_string}")
        quiz_id_completer = WordCompleter(striped_available_quizzes_list)
        quiz_id_validator = QuizIdValidator(striped_available_quizzes_list)
        quiz_id = self.quiz_id_prompt_session.prompt("What quiz would you like to add a question to? ",
                                                     completer=quiz_id_completer, validator=quiz_id_validator,
                                                     validate_while_typing=True, key_bindings=self.bindings)
        return quiz_id

    def ask_for_question(self):
        question = self.ask_for_question_question()
        incorrect_answers_count = self.ask_for_incorrect_answer_amount()
        incorrect_answers = self.ask_for_incorrect_answers(incorrect_answers_count)
        correct_answer = self.ask_for_correct_answer()
        question_id = generate_unique_id()
        question = {
            "question": question,
            "question_id": question_id,
            "incorrect_answers": incorrect_answers,
            "correct_answer": correct_answer
        }
        return question

    def ask_for_question_question(self):
        return self.question_prompt_session.prompt("Question: ")

    def ask_for_incorrect_answer_amount(self):
        return int(self.question_prompt_session.prompt("How many incorrect answers: "))

    def ask_for_incorrect_answers(self, incorrect_answer_amount: int):
        incorrect_answers = []
        for count in range(1, incorrect_answer_amount + 1):  # Loop for how may incorrect answers there is going to be
            incorrect_answers.append(self.question_prompt_session.prompt(f"Incorrect Answer {count}: "))
        return incorrect_answers

    def ask_for_correct_answer(self):
        return self.question_prompt_session.prompt("Correct Answer: ")

    def get_quiz_file(self, quiz_id):
        quiz_files = get_quiz_files(self.question_folder)
        try:
            return [i for i in quiz_files if i.startswith(quiz_id)][0]
        except IndexError:
            print(f"Could not find {quiz_id} question file. It may have been deleted.")
            exit(1)


class QuizIdValidator(Validator):
    def __init__(self, quiz_id_list):
        self.quiz_id_list = quiz_id_list

    def validate(self, document):
        if document.text not in self.quiz_id_list:
            raise ValidationError(message="Sorry that is not a valid quiz.")