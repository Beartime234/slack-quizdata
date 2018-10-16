"""This file contains helpers used in both uploading and testing the questions.
"""
import yaml
import os
from sys import exit
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


def load_file(file_path) -> str:
    """Loads a file from a path.

    Args:
        file_path: The full file path

    Returns:
        A string of the files contents
    """
    with open(file_path, 'r') as f:
        file_contents = f.read()
    return file_contents


def load_local_yaml(file_path) -> dict:
    """Loads a yaml file from a full file path

    Args:
        file_path: The full file path

    Returns:
        A dictionary of the files contents
    """
    return yaml.safe_load(load_file(file_path))


def save_local_yaml(file_path, data) -> dict:
    """Saves a yaml file

    Args:
        data: The data you wish to save
        file_path: The full file path

    Returns:
        A dictionary of the files contents
    """
    with open(file_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def is_ci_environ() -> bool:
    """This checks if we are running in the CI environment

    Returns:
        A boolean of true if in the CI environment otherwise returns false
    """
    return "CI" in os.environ


def generate_unique_id() -> str:
    """This functions generates a unique id and returns it

    Returns:
        A string of the unique id
    """
    return str(uuid4())


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


def key_exists(dictionary: dict, key: str) -> bool:
    """Checks that a key exists in a dictionary

    Args:
        dictionary: The dictionary that you are checking the key exists in
        key: The key that you are looking for

    Returns:
        A boolean True if it exists False if not
    """
    return key in dictionary.keys()


def value_is_string(value) -> bool:
    """Checks that the value is a string

    Args:
        value: The value that you are checking is a string

    Returns:
        Either true or false depending on if the value is a string

    """
    return isinstance(value, str)


def is_question_file_format(filename: str) -> bool:
    """Checks that a file is in a question file format

    Args:
        filename: The filename you are checking

    Returns:
        True if in a workable file format for questions False otherwise
    """
    return filename.endswith(".yml") or filename.endswith(".yaml")


def get_quiz_storage_table_environment_variable():
    quiz_question_table = ""
    try:
        quiz_question_table = os.environ["QUIZ_STORAGE_TABLE"]
    except KeyError:
        logger.critical("QUIZ_STORAGE_TABLE environment variable is not set.")
        exit(1)
    return quiz_question_table


def get_question_data(file_path):
    file_data = []
    try:
        file_data = load_local_yaml(file_path)["questions"]
    except FileNotFoundError as missing_file_error:
        logger.error(f"File: {file_path} could not be found. Error: {missing_file_error}")
        exit(1)
    except KeyError as missing_questions_map_error:
        logger.error(f"File: {file_path} does not have any questions. Error: {missing_questions_map_error}")
        exit(1)
    return file_data