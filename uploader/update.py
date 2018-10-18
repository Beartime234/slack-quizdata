"""This controls the main
"""
import logging.config
import os

import boto3

from uploader import QUESTION_FOLDER
from uploader import helpers

logger = logging.getLogger(__name__)


def upload():
    logger.info("Starting Upload")
    logger.info("Getting Quiz Table")
    # The table to load data into
    quiz_question_table: str = helpers.get_quiz_storage_table_environment_variable()
    quiz_table = boto3.resource("dynamodb").Table(quiz_question_table)
    # The following uploads the information
    logger.info("Starting upload of questions")
    for filename in helpers.get_quiz_files(QUESTION_FOLDER):
        full_file_path = f"{QUESTION_FOLDER}{filename}"
        file_data = helpers.get_question_data(full_file_path)
        logger.info(f"Uploading {filename}")
        load_data_into_table(
            quiz_table=quiz_table,
            quiz_id=filename.split(".")[0],
            questions=file_data
        )
    logger.info("Successfully uploaded questions to database")


def load_data_into_table(quiz_table: boto3.resource, quiz_id: str, questions: list) -> None:
    """Loads data into the designated quiz table

    Args:
        quiz_table: The name of the quiz table
        quiz_id: The id of the quiz. This will be assigned to the database quizId field.
        questions: The list of questions
    """
    with quiz_table.batch_writer() as batch:
        for question in questions:
            # Format the question correctly for how the quiz expects it and the slack quiz dynamodb table will read it
            configured_question = configure_question_for_upload(question, quiz_id)
            batch.put_item(Item=configured_question)  # Finally put the item in the database
    logger.info(f"Uploaded {len(questions)} questions to database")
    return


def configure_question_for_upload(question: dict, quiz_id: str) -> dict:
    """This function configures the question correctly for what the dynamodb expects.

    This is to make sure the YAML is readable for a user but the table knows what each value is.

    Args:
        question: The actual question dictionary
        quiz_id: The quiz-id that it will be using to set the id

    Returns:
        The question configured correctly for upload
    """
    temp_question = question.copy()  # Copy the question
    temp_question["id"] = get_question_id(quiz_id)  # Set the quiz id to be the quiz id specified by filename
    temp_question["range"] = get_question_range(temp_question.pop("question_id"))  # Set the id to be the question range
    return temp_question


def get_question_id(quiz_id: str) -> str:
    """Gets the question id from the quiz id

    Args:
        quiz_id: The quiz id

    Returns:
        The quiz-id string that is used in the table
    """
    return f"{quiz_id}-question"


def get_question_range(question_id: str) -> str:
    """The questions range which is just the questions id

    Args:
        question_id: The questions id so that we set that as the range

    Returns:
        The question_id
    """
    return question_id


if __name__ == '__main__':
    upload()
