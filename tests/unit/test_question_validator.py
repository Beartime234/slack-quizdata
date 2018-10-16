import pytest
from uploader import question_validator
from tests.unit.test_values import question_examples

test_question = question_examples.good_question


def test_check_question():
    assert question_validator.check_question(test_question, []) is None
