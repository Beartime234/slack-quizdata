good_question = {
    "correct_answer": "Lickitung",
    "incorrect_answers": [
        "Digimon",
        "Tiger",
        "Sphagetti"
    ],
    "question": "Which of the following is a Pokemon?",
    "question_id": "dad387e2-959a-4aba-9ef6-d99a8ba9bfbf"
}

test_quiz_id = "testquiz"

good_question_configured = good_question.copy()
good_question_configured["id"] = "testquiz-question"
good_question_configured["range"] = good_question_configured.pop("question_id")

good_question_list = [
    good_question
]
