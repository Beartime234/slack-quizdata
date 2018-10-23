"""Application for creating questions
"""

from uploader.creator import QuestionCreator
from uploader import QUESTION_FOLDER

if __name__ == '__main__':
    QuestionCreator(QUESTION_FOLDER).run()
