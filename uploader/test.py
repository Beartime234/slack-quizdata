import logging
import os
import sys

from uploader import QUESTION_FOLDER
from uploader import helpers, exceptions

logger = logging.getLogger(__name__)


def test():
    logger.info("Starting test of Questions")
    # Loop through each of the files in the questions of the directory
    logger.info("Starting check of questions")
    for filename in os.listdir(QUESTION_FOLDER):
        if filename.endswith(".yml"):
            full_file_path = f"{QUESTION_FOLDER}{filename}"
            file_data = helpers.load_local_yaml(full_file_path)["questions"]
            check_questions(file_data)
        else:
            continue
    logger.info("Finished test was successful")


def check_questions(questions: list):
    """Checks all questions

    Args:
        questions: The questions list
    """
    for question in questions:
        try:
            check_question(question)  # Check the question
        except exceptions.BadQuestion as bad_exception:  # If it's bad move to the next question and log it
            logger.critical(f"Question - {question} is bad {bad_exception}")
            sys.exit(1)  # Exit badly and stored


def check_question(question):
    """Check the question to make sure that it is configured correctly

    Args:
        question: The question itself
    """
    if "incorrect_answers" not in question.keys():
        raise exceptions.BadQuestion("no incorrect Answers")
    if "question" not in question.keys():
        raise exceptions.BadQuestion("no question")
    if "correct_answer" not in question.keys():
        raise exceptions.BadQuestion("no correct answer")
    if len(question["incorrect_answers"]) > 4:
        raise exceptions.BadQuestion(f"question has too many incorrect answers. {question}")
    for answer in question["incorrect_answers"]:
        if not isinstance(answer, str):
            raise TypeError(f"unsupported type  - all answers must be strings. {question}")
    if not isinstance(question["correct_answer"], str):
        raise TypeError(f"unsupported type  - all answers must be strings. {question}")
    return


if __name__ == '__main__':
    test()
