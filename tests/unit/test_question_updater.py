import pytest
from uploader import question_updater
from tests.unit.test_values import question_examples

test_question = question_examples.good_question
test_question_list = question_examples.good_question_list
test_question_configured = question_examples.good_question_configured
test_quiz_id = question_examples.test_quiz_id


def test_configure_question_for_upload():
    ret = question_updater.configure_question_for_upload(test_question, test_quiz_id)
    assert ret == test_question_configured


def test_get_question_id():
    assert question_updater.get_question_id(test_quiz_id) == "testquiz-question"


def test_get_question_range():
    question_id = "random"
    assert question_updater.get_question_range(question_id) == question_id
