from .quiz_register import QuizRegister
from .answer_register import AnswerRegister


class Quiz:
    def __init__(self, quiz_id, title, question, active, category=None):
        self.quiz_id = quiz_id
        self.title = title
        self.question = question
        self.active = active
        self.category = category
        # get answers from quiz id from database table answer join them


    

    # def make_quiz():
    #     with QuizRegister as db:
    #         db.create_quiz()