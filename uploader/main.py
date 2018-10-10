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
        logger.critical("QUIZ_QUESTION_TABLE Environment Variable Is Not Set")
        sys.exit(1)
    quiz_table = boto3.resource("dynamodb").Table(quiz_question_table)
    # Does a check of the questions before uploading them
    logger.info("Starting upload of questions")
    for filename in os.listdir(QUESTION_FOLDER):
        if filename.endswith(".yml"):
            full_file_path = f"{QUESTION_FOLDER}{filename}"
            file_data = helpers.load_local_yaml(full_file_path)["questions"]
            logger.info(f"Uploading {filename}")
            data = load_data_into_table(
                quiz_table,
                filename.split(".yml")[0],
                file_data
            )
            logger.info(f"Updating {filename}")
            helpers.save_local_yaml(
                full_file_path,
                {"questions": data}
            )
        else:
            continue
    logger.info("Finished uploading questions to database")


def load_data_into_table(quiz_table, quiz_id: str, questions: dict):
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
            temp_question["quizId"] = quiz_id  # Set the quiz id to be the quiz id specified by filename
            temp_question["questionRange"] = temp_question.pop("id")  # Set the id to be the question range
            batch.put_item(Item=temp_question)  # Finally put the item in the database
    logger.info(f"Uploaded {len(questions)} questions to database")
    return questions  # Return the questions because we need to resave them


def check_if_id_in_question(question):
    return "id" in question.keys()


def add_id_to_question(question):
    question["id"] = str(uuid4())
    return question


if __name__ == '__main__':
    upload()
