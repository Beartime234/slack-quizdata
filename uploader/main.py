"""This controls the main
"""
import logging.config
import os
from uuid import uuid4
import sys

import boto3

from uploader import QUESTION_FOLDER
from uploader import helpers

logger = logging.getLogger(__name__)


def upload():
    logger.info("Starting Upload")
    logger.info("Getting Quiz Table")
    # The table to load data into
    try:
        quiz_question_table = os.environ["QUIZ_STORAGE_TABLE"]
    except KeyError:
        logger.critical("QUIZ_STORAGE_TABLE environment variable is not set. This is a problem with your configuration"
                        "or build pipeline")
        sys.exit(1)
    quiz_table = boto3.resource("dynamodb").Table(quiz_question_table)
    # The following uploads the information
    logger.info("Starting upload of questions")
    filename: str  # Set this to a string cause we are using it that way
    for filename in os.listdir(QUESTION_FOLDER):
        if filename.endswith(".yml"):
            full_file_path = f"{QUESTION_FOLDER}{filename}"
            file_data = helpers.load_local_yaml(full_file_path)["questions"]
            logger.info(f"Uploading {filename}")
            data = load_data_into_table(
                quiz_table=quiz_table,
                quiz_id=filename.split(".yml")[0],
                questions=file_data
            )
            logger.info(f"Updating {filename}")
            # This re-saves the file because some id's will be created.
            helpers.save_local_yaml(
                full_file_path,
                {"questions": data}
            )
        else:
            continue
    logger.info("Finished uploading questions to database")


def load_data_into_table(quiz_table: boto3.resource, quiz_id: str, questions: list) -> object:
    """Loads data into the designated quiz table

    Args:
        quiz_table: The name of the quiz table
        quiz_id: The id of the quiz. This will be assigned to the database quizId field.
        questions: The list of questions

    Returns:
        Will return the new data and should be resaved into the same file as it will have the questions designated id
    """
    with quiz_table.batch_writer() as batch:
        # First check that all the questions are good
        for question in questions:
            if not check_if_id_in_question(question):  # If it doesn't have an id assign one to it
                add_id_to_question(question)
            # Format the question correctly for how the quiz expects it and dynamodb will read it
            temp_question = question.copy()  # Copy the question so we don't return the copy and we keep it readable
            temp_question["id"] = f"{quiz_id}-question"  # Set the quiz id to be the quiz id specified by filename
            temp_question["range"] = temp_question.pop("question_id")  # Set the id to be the question range
            batch.put_item(Item=temp_question)  # Finally put the item in the database
    logger.info(f"Uploaded {len(questions)} questions to database")
    return questions  # Return the questions because we need to resave them


def check_if_id_in_question(question: dict) -> bool:
    """This checks if there is a question id in the question.

    Args:
        question:

    Returns:
        If there is will return True otherwise will return false
    """
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
    upload()
