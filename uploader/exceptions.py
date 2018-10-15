class BadQuestion(Exception):
    """Top level exception for a bad question
    """
    pass


class BuildQuestionWithoutID(BadQuestion):
    """This exception represents that the question was without an ID in the build stage
    """
    pass


class NoIncorrectAnswers(BadQuestion):
    """This exception represents that there was no incorrect answers for this question
    """
    pass


class NoQuestion(BadQuestion):
    """This exception represents that there was no question for this question
    """
    pass


class NoCorrectAnswer(BadQuestion):
    """This exception represents that there was no question for this question
    """
    pass


class TooManyIncorrectAnswers(BadQuestion):
    """This exception represents that there was too many incorrect answers
    """
    pass


class NotStringedQuestion(BadQuestion):
    """This exception represents that one of the question, incorrect answer or correct answer is not a string
    """
    pass


class DuplicateQuestionID(BadQuestion):
    """This exception represents that one of the questions has a duplicate id. This shouldn't happen but I check anyway
    """
    pass
