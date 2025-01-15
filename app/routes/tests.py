from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import MockTest, Question, Answer, TestResult
from app import db

bp = Blueprint('tests', __name__, url_prefix='/tests')

@bp.route('/')
@login_required
def index():
    tests = MockTest.query.all()
    return render_template('tests/index.html', tests=tests)

@bp.route('/<int:test_id>')
@login_required
def take_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    return render_template('tests/take_test.html', test=test)

@bp.route('/<int:test_id>/submit', methods=['POST'])
@login_required
def submit_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    data = request.get_json()
    
    # Calculate score
    score = 0
    # Add score calculation logic here
    
    # Save test result
    result = TestResult(
        user_id=current_user.id,
        mock_test_id=test_id,
        score=score
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'score': score}) 