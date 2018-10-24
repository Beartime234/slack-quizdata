"""This is a small python program that helps user add questions so that they don't make mistakes and makes it easier
for them
"""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator, ValidationError
from pyfiglet import figlet_format
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from uploader.helpers import get_quiz_files, generate_unique_id, save_question_to_question_file, form_question


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
        self.bindings = KeyBindings()
        self.quiz_id_prompt_session = PromptSession(key_bindings=self.bindings)
        self.question_prompt_session = PromptSession(key_bindings=self.bindings)
        self.amount_of_incorrect_answer_session = PromptSession(key_bindings=self.bindings)
        self.incorrect_answer_session = PromptSession(key_bindings=self.bindings)
        self.correct_answer_session = PromptSession(key_bindings=self.bindings)

        @self.bindings.add('c-q')  # This just makes the program exit nice when the user holds down control and Q
        def _(event):
            event.app.exit()

    def run(self):
        """Runs the app
        """
        self.print_intro_message()
        quiz_id = self.request_quiz_id()
        print("\n")
        question_file = self.get_quiz_file(quiz_id)
        go_again = True
        while go_again is True:
            question = self.ask_for_question()
            print("Saved Question")
            save_question_to_question_file(question, f"{self.question_folder}{question_file}")
            go_again = self.ask_if_go_again()

    def print_intro_message(self):
        """Prints the introduction message
        """
        print(figlet_format(self.creator_name))
        print("Press Control + Q at any time to quit")
        print("\n")

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
        quiz_id = self.quiz_id_prompt_session.prompt("What quiz would you like to add questions to? ",
                                                     completer=quiz_id_completer, validator=quiz_id_validator,
                                                     validate_while_typing=False)
        return quiz_id

    def ask_for_question(self) -> dict:
        """Main holder for asking a question. Will prompt the user for all relevant information for the question
        Returns:
            The dictionary of the well formed question
        """
        question = self.ask_for_question_question()
        incorrect_answers_count = self.ask_for_incorrect_answer_amount()
        incorrect_answers = self.ask_for_incorrect_answers(incorrect_answers_count)
        correct_answer = self.ask_for_correct_answer()
        question_id = generate_unique_id()
        return form_question(question, question_id, incorrect_answers, correct_answer)

    def ask_for_question_question(self):
        """Asks the user for their question
        """
        return str(self.question_prompt_session.prompt("Question: "))

    def ask_for_incorrect_answer_amount(self):
        """Asks the user for how many incorrect answers they can have
        """
        completer = WordCompleter(["1", "2", "3", "4"])
        return int(self.question_prompt_session.prompt("How many incorrect answers: ", completer=completer,
                                                       validator=IncorrectAnswerValidator()))

    def ask_for_incorrect_answers(self, incorrect_answer_amount: int):
        """Ask for the users incorrect answers for the question

        Args:
            incorrect_answer_amount: The amount of incorrect answers

        Returns:
            A list of the users incorrect answers
        """
        incorrect_answers = []
        for count in range(1, incorrect_answer_amount + 1):  # Loop for how may incorrect answers there is going to be
            incorrect_answers.append(str(self.incorrect_answer_session.prompt(f"> Incorrect Answer {count}: ")))
        return incorrect_answers

    def ask_for_correct_answer(self):
        """Asks the user for the correct answer

        Returns:
            The correct answer as a string
        """
        return str(self.correct_answer_session.prompt("Correct Answer: "))

    def get_quiz_file(self, quiz_id: str):
        """Gets the appropriate quiz_file based on id

        Args:
            quiz_id: The quiz id

        Returns:
            The filename of the appropriate quiz
        """
        quiz_files = get_quiz_files(self.question_folder)
        try:
            return [i for i in quiz_files if i.startswith(quiz_id)][0]
        except IndexError:
            print(f"Could not find {quiz_id} question file. It may have been deleted.")
            exit(1)

    def ask_if_go_again(self) -> bool:
        """Asks the user if they want to go again

        Returns:
            A boolean of true and false if they want to go again
        """
        allowed_go_again_values = ["yes", "y", "no", "n"]
        go_again_completer = WordCompleter(allowed_go_again_values)
        go_again_validator = GoAgainValidator(allowed_go_again_values)
        go_again: str = self.quiz_id_prompt_session.prompt("Would you like to add another question? ",
                                                           completer=go_again_completer, validator=go_again_validator,
                                                           validate_while_typing=False)
        go_again = go_again.lower()
        if go_again == "yes" or go_again == "y":
            return True
        else:
            return False


class QuizIdValidator(Validator):
    def __init__(self, quiz_id_list):
        self.quiz_id_list = quiz_id_list

    def validate(self, document):
        text = document.text
        if text not in self.quiz_id_list:
            raise ValidationError(message="Sorry that is not a valid quiz.", cursor_position=len(text))


class GoAgainValidator(Validator):
    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    def validate(self, document):
        text = document.text

        if text not in self.allowed_values:
            raise ValidationError(message="The input must be yes/y or no/n", cursor_position=len(text))


class IncorrectAnswerValidator(Validator):
    def validate(self, document):
        text = document.text

        if len(text) != 1:
            raise ValidationError(message="Value should be between 1 - 4", cursor_position=len(text))

        if text and not text.isdigit():  # Check if the entire thing is numberic/digits
            for i, c in enumerate(text):
                if not c.isdigit():
                    raise ValidationError(message='This input contains non-numeric characters',
                                          cursor_position=i)

        if int(text) > 4 or int(text) < 1:
            raise ValidationError(message="Value should be between 1 - 4", cursor_position=len(text))



