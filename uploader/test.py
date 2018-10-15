"""This file runs tests on the questions file. It does not perform tests on the code.
but instead makes sure that the questions
"""
import logging
import os
import sys
from uuid import uuid4

from uploader import QUESTION_FOLDER
from uploader import helpers, exceptions

logger = logging.getLogger(__name__)


def test():
    # Loop through each of the files in the questions of the directory
    logger.info("Starting check of questions")
    for filename in os.listdir(QUESTION_FOLDER):
        if filename.endswith(".yml"):  # if the file ends with yml check the questions that exist
            full_file_path = f"{QUESTION_FOLDER}{filename}"
            file_data = helpers.load_local_yaml(full_file_path)["questions"]
            logger.info(f"Checking {filename}")
            questions = check_questions(file_data)
            logger.info(f"Updating {filename}")
            # This re-saves the file because some id's will be created. if it
            helpers.save_local_yaml(
                full_file_path,
                {"questions": questions}
            )
        else:  # Ignore anything else
            continue
    logger.info("Test of questions was successful")


def check_questions(questions: list):
    """Checks all questions

    Args:
        questions: The questions list
    """
    id_list = []
    for question in questions:
        try:
            if not check_if_id_in_question(question):  # If it doesn't have an id assign one to it
                add_id_to_question(question)
            check_question(question, id_list)  # Check the question
            id_list.append(question["question_id"])  # Append this questions ID
        except exceptions.BadQuestion as bad_question_exception:  # If it's bad exit
            logger.critical(f"Question - {question} is bad {bad_question_exception}")
            sys.exit(1)  # Exit badly
    return questions


def check_question(question: dict, id_list: list):
    """Check the question to make sure that it is configured correctly

    Args:
        id_list: A list of ids that have already been checked
        question: The question itself
    """
    if "incorrect_answers" not in question.keys():  # First make sure there are some incorrect answers
        raise exceptions.NoIncorrectAnswers()
    if "question" not in question.keys():  # Make sure that there is actually a question
        raise exceptions.NoQuestion()
    if "correct_answer" not in question.keys():  # Make sure there is a correct answer
        raise exceptions.NoCorrectAnswer()
    if len(question["incorrect_answers"]) > 4:  # Make sure there is no more then 4 correct answers
        raise exceptions.TooManyIncorrectAnswers()
    for answer in question["incorrect_answers"]:  # Make sure all the incorrect answers are strings
        if not isinstance(answer, str):
            raise exceptions.NotStringedQuestion()
    if not isinstance(question["correct_answer"], str):  # Make sure the correct answer is a string
        raise exceptions.NotStringedQuestion()
    if not isinstance(question["question"], str):  # Make sure the question is a string
        raise exceptions.NotStringedQuestion()
    if question["question_id"] in id_list:
        raise exceptions.DuplicateQuestionID()
    return


def check_if_id_in_question(question: dict) -> bool:
    """This checks if there is a question id in the question.

    Args:
        question:

    Returns:
        If there is will return True otherwise will return false
    """
    if "question_id" not in question.keys():
        if helpers.is_ci_environ():  # If we are in the build environment then every question should have an ID ]
            raise exceptions.BuildQuestionWithoutID()
    return "question_id" in question.keys()


def add_id_to_question(question: dict) -> dict:
    """This function add's an id to the question.

    Args:
        question: The question dictionary

    Returns:
        The same dictionary with a new field question_id with a uuid4 attached to it.
    """
    question["question_id"] = str(uuid4())
    return question


if __name__ == '__main__':
    test()
