"""This file runs tests on the questions file. It does not perform tests on the code.
but instead makes sure that the questions are valid.
"""
import logging

from uploader import QUESTION_FOLDER
from uploader import helpers
from uploader.checker import question_checks

logger = logging.getLogger(__name__)


def test():
    """This function performs tests on question files that end with.yml

    This is the main function that is used when testing that questions are valid.
    It will resave the file if there are missing ids in the question.
    """
    # Loop through each of the files in the questions of the directory
    logger.info("Starting validation check of questions.")
    for filename in helpers.get_quiz_files(QUESTION_FOLDER):
        full_file_path = f"{QUESTION_FOLDER}{filename}"
        file_data = helpers.get_question_data(full_file_path)
        logger.info(f"Checking {filename}")
        updated_questions = check_questions(file_data)
        # This re-saves the file if we are not in build because some question id's will be created.
        # if they didn't have one.
        if not helpers.is_ci_environ():
            save_questions_file(full_file_path, updated_questions)
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


def save_questions_file(file_path: str, questions_list: list) -> None:
    logger.info(f"Saving {file_path}")
    helpers.save_local_yaml(
        file_path,
        {"questions": questions_list}
    )
    return


if __name__ == '__main__':
    test()
