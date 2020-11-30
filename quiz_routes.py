import models
from flask import Blueprint, jsonify, request, abort
import user_session_manager

quiz_routes = Blueprint('quiz_routes', __name__, template_folder='templates')


@quiz_routes.route('/_apis/quiz', methods=['GET'])
@user_session_manager.require_login
@user_session_manager.report_activity
def all_quizzes():
    quizzes = models.Quiz.query.all()
    quizzes_schema = models.QuizSchema(many=True)
    quizzes_json = quizzes_schema.dumps(quizzes)
    return quizzes_json


@quiz_routes.route('/_apis/quiz/<quiz_id>/questions', methods=['GET'])
@user_session_manager.require_login(get_permission=True)
@user_session_manager.report_activity
def get_quiz_questions(quiz_id, permission=None):
    quiz = models.Quiz.query.get(quiz_id)

    if not quiz:
        return abort(404)

    questions_schema = models.QuestionSchema(many=True)
    dict_questions = questions_schema.dump(quiz.questions)

    for question in dict_questions:
        answers = []
        for key in ['answer_' + letter for letter in 'abcde']:
            if question[key] is not None:
                answers.append(question[key])
            del question[key]

        if permission.lower() in ('view', 'edit'):
            question['answers'] = answers

    return jsonify(dict_questions)


@quiz_routes.route('/_apis/quiz/<quiz_id>', methods=['GET'])
@user_session_manager.require_login
@user_session_manager.report_activity
def get_quiz(quiz_id):
    quiz = models.Quiz.query.get(quiz_id)
    quiz_schema = models.QuizSchema()
    quiz_json = quiz_schema.dumps(quiz)
    return quiz_json


@quiz_routes.route('/_apis/quiz', methods=['POST'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def create_quiz():
    data = request.get_json()
    quiz_schema = models.QuizSchema()

    quiz = quiz_schema.load(dict(title=data['title']), session=models.db.session)
    models.db.session.add(quiz)
    models.db.session.commit()

    quiz_json = quiz_schema.dumps(quiz)
    return quiz_json, 201


@quiz_routes.route('/_apis/quiz/<quiz_id>/questions', methods=['POST'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def create_question(quiz_id):
    data = request.get_json()
    answers = {'answer_' + 'abcde'[i]: answer for i, answer in enumerate(data['answers'][:5])}

    question_schema = models.QuestionSchema()
    question = question_schema.load(dict(quiz_id=quiz_id, question_text=data['question_text'],
                                         question_order=data['question_order'], **answers),
                                    session=models.db.session)

    models.db.session.add(question)
    models.db.session.commit()

    question_json = question_schema.dumps(question)
    return question_json, 201


@quiz_routes.route('/_apis/quiz/<quiz_id>', methods=['POST'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def update_quiz(quiz_id):
    data = request.get_json()
    quiz = models.Quiz.query.get(quiz_id)

    if not quiz:
        return abort(404)

    if data.get('title'):
        quiz.title = data['title']

    models.db.session.add(quiz)
    models.db.session.commit()

    quiz_schema = models.QuizSchema()
    quiz_json = quiz_schema.dumps(quiz)
    return quiz_json


@quiz_routes.route('/_apis/question/<question_id>', methods=['POST'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def update_question(question_id):
    data = request.get_json()
    question = models.Question.query.get(question_id)

    if not question:
        return abort(404)

    if data.get('question_text'):
        question.question_text = data['question_text']
    if data.get('question_order'):
        question.question_order = data['question_order']
    if data.get('answers'):
        question.answer_a = data['answers'][0]
        question.answer_b = data['answers'][1]
        question.answer_c = data['answers'][2]
        if len(data['answers']) > 3:
            question.answer_d = data['answers'][3]
        if len(data['answers']) > 4:
            question.answer_e = data['answers'][4]

    models.db.session.add(question)
    models.db.session.commit()

    question_schema = models.QuestionSchema()
    question_json = question_schema.dumps(question)
    return question_json


@quiz_routes.route('/_apis/quiz/<quiz_id>', methods=['DELETE'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def delete_quiz(quiz_id):
    quiz = models.Quiz.query.get(quiz_id)

    if not quiz:
        return abort(404)

    models.db.session.delete(quiz)
    models.db.session.commit()

    return jsonify(dict(success=True))


@quiz_routes.route('/_apis/question/<question_id>', methods=['DELETE'])
@user_session_manager.require_login(permissions=['edit'])
@user_session_manager.report_activity
def delete_question(question_id):
    question = models.Question.query.get(question_id)

    if not question:
        return abort(404)

    models.db.session.delete(question)
    models.db.session.commit()

    return jsonify(dict(success=True))
