import pytest
from uploader import question_validator
from tests.unit.test_values import question_examples

test_question = question_examples.good_question
test_question_list = question_examples.good_question_list


def test_check_question():
    assert question_validator.check_question(test_question, []) is None


# Should also test that it adds and saves ids
def test_check_questions():
    assert question_validator.check_questions(test_question_list) is test_question_list
