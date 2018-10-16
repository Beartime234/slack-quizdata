import pytest
from uploader import question_checks, exceptions
from tests.unit.test_values import question_examples

test_question = question_examples.good_question


def test_check_incorrect_answer_exists():
    assert question_checks.check_incorrect_answer_exists(test_question) is None
    test_question_error = test_question.copy()
    test_question_error.pop("incorrect_answers", None)
    with pytest.raises(exceptions.NoIncorrectAnswers):
        question_checks.check_incorrect_answer_exists(test_question_error)


def test_check_question_exists():
    assert question_checks.check_question_exists(test_question) is None
    test_question_error = test_question.copy()
    test_question_error.pop("question", None)
    with pytest.raises(exceptions.NoQuestion):
        question_checks.check_question_exists(test_question_error)


def test_check_correct_answer_exists():
    assert question_checks.check_correct_answer_exists(test_question) is None
    test_question_error = test_question.copy()
    test_question_error.pop("correct_answer", None)
    with pytest.raises(exceptions.NoCorrectAnswer):
        question_checks.check_correct_answer_exists(test_question_error)


def test_check_too_many_incorrect_answers():
    assert question_checks.check_too_many_incorrect_answers(test_question) is None
    test_question_error = test_question.copy()
    test_question_error["incorrect_answers"] = ["1", "2", "3", "4", "5"]
    with pytest.raises(exceptions.TooManyIncorrectAnswers):
        question_checks.check_too_many_incorrect_answers(test_question_error)


def test_check_incorrect_answers_are_string():
    assert question_checks.check_incorrect_answers_are_string(test_question) is None
    test_question_error = test_question.copy()
    test_question_error["incorrect_answers"] = ["1", "2", 3, "4", "5"]
    with pytest.raises(exceptions.NotStringedQuestionValue):
        question_checks.check_incorrect_answers_are_string(test_question_error)


def test_check_correct_answer_is_string():
    assert question_checks.check_correct_answer_is_string(test_question) is None
    test_question_error = test_question.copy()
    test_question_error["correct_answer"] = 3
    with pytest.raises(exceptions.NotStringedQuestionValue):
        question_checks.check_correct_answer_is_string(test_question_error)


def test_check_question_is_string():
    assert question_checks.check_question_is_string(test_question) is None
    test_question_error = test_question.copy()
    test_question_error["question"] = 3
    with pytest.raises(exceptions.NotStringedQuestionValue):
        question_checks.check_question_is_string(test_question_error)


def test_check_no_duplicate_question_id():
    assert question_checks.check_no_duplicate_question_id(test_question, []) is None
    test_question_error = test_question.copy()
    test_question_error["question_id"] = "1"
    with pytest.raises(exceptions.DuplicateQuestionID):
        question_checks.check_no_duplicate_question_id(test_question_error, ["1"])
