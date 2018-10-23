from uploader import helpers
from uploader.checker import exceptions


def check_incorrect_answer_exists(question: dict) -> None:
    """This checks that an incorrect answer exists in the question
    Args:
        question:

    Raises:
        NoIncorrectAnswers if there are no incorrect answers
    """
    if not helpers.key_exists(question, "incorrect_answers"):
        raise exceptions.NoIncorrectAnswers(question)
    return


def check_question_exists(question: dict) -> None:
    """This checks that the question exists in the question
    Args:
        question: The question dictionary

    Raises:
        NoQuestion if there are no incorrect answers
    """
    if not helpers.key_exists(question, "question"):
        raise exceptions.NoQuestion(question)
    return


def check_correct_answer_exists(question: dict) -> None:
    """This checks that a correct answer exists in the question
    Args:
        question: The question dictionary

    Raises:
        NoCorrectAnswer if there are no correct answers
    """
    if not helpers.key_exists(question, "correct_answer"):
        raise exceptions.NoCorrectAnswer(question)
    return


def check_too_many_incorrect_answers(question: dict) -> None:
    """This checks that there are not too many incorrect answers

    Args:
        question: The question dictionary

    Raises:
        TooManyIncorrectAnswers if there are no correct answers
    """
    if len(question["incorrect_answers"]) > 4:
        raise exceptions.TooManyIncorrectAnswers(question)


def check_incorrect_answers_are_string(question: dict) -> None:
    """This checks that all incorrect answers are a string

    Args:
        question: The question dictionary

    Raises:
        NotStringedQuestionValue if there are no correct answers
    """
    for answer in question["incorrect_answers"]:
        if not helpers.value_is_string(answer):
            raise exceptions.NotStringedQuestionValue(question)


def check_correct_answer_is_string(question: dict) -> None:
    """This checks that the correct answer is a string

    Args:
        question: The question dictionary

    Raises:
        NotStringedQuestionValue if the correct answer is a string
    """
    if not helpers.value_is_string(question["correct_answer"]):
        raise exceptions.NotStringedQuestionValue(question)


def check_question_is_string(question: dict) -> None:
    """This checks that the question is a string

    Args:
        question: The question dictionary

    Raises:
        NotStringedQuestionValue if the correct answer is a string
    """
    if not helpers.value_is_string(question["question"]):
        raise exceptions.NotStringedQuestionValue(question)


def check_no_duplicate_question_id(question: dict, id_list: list):
    """Checks that there are no duplicate question ids

    Args:
        question: The question itself
        id_list: A list of id's that should exist

    Raises:
        DuplicateQuestionID if there is a duplicate id
    """
    if question["question_id"] in id_list:
        raise exceptions.DuplicateQuestionID(question)
