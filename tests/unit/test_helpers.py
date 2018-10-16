import pytest
from uploader import helpers


def test_generating_unique_id():
    ret = helpers.generate_unique_id()
    assert type(ret) == str


def test_check_if_id_in_question():
    question_without_id = {"question": "blah"}
    ret_without = helpers.check_if_id_in_question(question_without_id)
    assert ret_without is False
    question_with_id = {"question_id": "somerandomid"}
    ret_with = helpers.check_if_id_in_question(question_with_id)
    assert ret_with is True


def test_add_id_to_question():
    question = {
        "question": "What is a dog?",
        "incorrect_answers": [],
        "correct_answer": ""
    }
    ret = helpers.add_id_to_question(question)
    assert "question_id" in ret.keys()
    assert type(question["question_id"]) is str


def test_key_exists():
    test_dict = {
        "key": "value"
    }
    ret = helpers.key_exists(test_dict, "key")
    assert ret is True
    ret = helpers.key_exists(test_dict, "random")
    assert ret is False


def test_value_is_string():
    value_str = "random"
    value_int = 0
    value_bool = False
    value_list = []
    value_dict = {}
    assert helpers.value_is_string(value_str) is True
    assert helpers.value_is_string(value_int) is False
    assert helpers.value_is_string(value_bool) is False
    assert helpers.value_is_string(value_list) is False
    assert helpers.value_is_string(value_dict) is False
