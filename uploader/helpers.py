"""This file contains helpers used in both uploading and testing the questions.
"""
import yaml
import os
from uuid import uuid4


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
