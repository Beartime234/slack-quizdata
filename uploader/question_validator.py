"""This file runs tests on the questions file. It does not perform tests on the code.
but instead makes sure that the questions
"""
import logging
import os

from uploader import QUESTION_FOLDER
from uploader import helpers, exceptions, question_checks

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
            # This re-saves the file if we are not in build because some id's will be created. if they didn't have one.
            if not helpers.is_ci_environ():
                logger.info(f"Updating {filename}")
                helpers.save_local_yaml(
                    full_file_path,
                    {"questions": questions}
                )
        else:  # Ignore anything else
            continue
    logger.info("Test of questions was successful. Questions are valid.")


def check_questions(questions: list):
    """Checks all questions

    Args:
        questions: The questions list

    Returns:
        The questions list with any addeded Id's to it
    """
    id_list = []
    for question in questions:
        if not helpers.check_if_id_in_question(question):  # If it doesn't have an id assign one to it
            helpers.add_id_to_question(question)
        check_question(question, id_list)  # Check the question
        id_list.append(question["question_id"])  # Append this questions ID
    return questions


def check_question(question: dict, id_list: list):
    """Check the question to make sure that it is configured correctly

    Args:
        id_list: A list of ids that have already been checked
        question: The question itself
    """
    question_checks.check_incorrect_answer_exists(question)  # First make sure there are some incorrect answers
    question_checks.check_question_exists(question)
    question_checks.check_correct_answer_exists(question)
    question_checks.check_too_many_incorrect_answers(question)
    question_checks.check_incorrect_answers_are_string(question)
    question_checks.check_correct_answer_is_string(question)
    question_checks.check_question_is_string(question)
    question_checks.check_no_duplicate_question_id(question, id_list)
    return


if __name__ == '__main__':
    test()
