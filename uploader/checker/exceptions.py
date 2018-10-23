"""This file contains the exceptions if one of the questions is misconfigured.
"""


class BadQuestion(Exception):
    """Top level exception for a bad question
    """

    def __init__(self, question):
        message = f"{self.__class__.__name__} Question: {question} "

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class BuildQuestionWithoutID(BadQuestion):
    """This exception represents that the question was without an ID in the build stage
    """

    def __init__(self, question):
        message = f"Question {question} is in CI and does not have a ID. Each question should have a unique ID when " \
                  f"committed. "
        super().__init__(message)


class NoIncorrectAnswers(BadQuestion):
    """This exception represents that there was no incorrect answers for this question
    """

    def __init__(self, question):
        message = f"Question {question} does not have any incorrect answers."
        super().__init__(message)


class NoQuestion(BadQuestion):
    """This exception represents that there was no question for this question
    """

    def __init__(self, question):
        message = f"Question {question} does not have a question."
        super().__init__(message)


class NoCorrectAnswer(BadQuestion):
    """This exception represents that there was no question for this question
    """

    def __init__(self, question):
        message = f"Question {question} does not have a correct answer."
        super().__init__(message)


class TooManyIncorrectAnswers(BadQuestion):
    """This exception represents that there was too many incorrect answers
    """

    def __init__(self, question):
        message = f"Question {question} has too many incorrect answers."
        super().__init__(message)


class NotStringedQuestionValue(BadQuestion):
    """This exception represents that one of the question, incorrect answer or correct answer is not a string
    """

    def __init__(self, question):
        message = f"Question {question} one of the fields is not a string."
        super().__init__(message)


class DuplicateQuestionID(BadQuestion):
    """This exception represents that one of the questions has a duplicate id. This shouldn't happen but I check anyway
    """

    def __init__(self, question):
        message = f"Question {question} has the same ID as another question."
        super().__init__(message)
