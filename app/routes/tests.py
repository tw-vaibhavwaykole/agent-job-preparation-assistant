from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import MockTest, Question
from app import db

bp = Blueprint('tests', __name__, url_prefix='/tests')

@bp.route('/list')
@login_required
def list():
    tests = MockTest.query.all()
    return render_template('tests/list.html', tests=tests)

@bp.route('/<int:id>')
@login_required
def take_test(id):
    test = MockTest.query.get_or_404(id)
    return render_template('tests/take.html', test=test)

@bp.route('/<int:id>/submit', methods=['POST'])
@login_required
def submit_test(id):
    test = MockTest.query.get_or_404(id)
    answers = request.get_json()
    score = 0
    for question in test.questions:
        if str(question.id) in answers:
            if answers[str(question.id)] == question.correct_answer:
                score += 1
    return jsonify({'score': score, 'total': len(test.questions)}) 