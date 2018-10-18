import pytest
from uploader import validate
from tests.unit.test_values import question_examples

test_question = question_examples.good_question
test_question_list = question_examples.good_question_list


def test_check_question():
    assert validate.check_question(test_question, []) is None


# Should also test that it adds and saves ids
def test_check_questions():
    assert validate.check_questions(test_question_list) is test_question_list
