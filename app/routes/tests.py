from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import MockTest, Question, Answer, TestResult

tests_bp = Blueprint('tests', __name__)

@tests_bp.route('/tests', methods=['GET'])
@login_required
def list_tests():
    db = current_app.db.session
    tests = db.query(MockTest).all()
    return jsonify([test.to_dict() for test in tests])

@tests_bp.route('/tests/<int:test_id>', methods=['GET'])
@login_required
def get_test(test_id):
    db = current_app.db.session
    test = db.query(MockTest).filter(MockTest.id == test_id).first()
    if not test:
        return jsonify({'error': 'Test not found'}), 404
    return jsonify(test.to_dict())

@tests_bp.route('/tests/<int:test_id>/start', methods=['POST'])
@login_required
def start_test(test_id):
    db = current_app.db.session
    test = db.query(MockTest).filter(MockTest.id == test_id).first()
    if not test:
        return jsonify({'error': 'Test not found'}), 404
    
    # Get questions for the test
    questions = db.query(Question).filter(Question.test_id == test_id).all()
    return jsonify({
        'test': test.to_dict(),
        'questions': [q.to_dict() for q in questions]
    })

@tests_bp.route('/tests/<int:test_id>/submit', methods=['POST'])
@login_required
def submit_test(test_id):
    db = current_app.db.session
    answers_data = request.json.get('answers', [])
    
    total_marks = 0
    for answer_data in answers_data:
        answer = Answer(
            question_id=answer_data['question_id'],
            user_id=current_user.id,
            answer_text=answer_data['answer_text']
        )
        db.add(answer)
        
        # Calculate marks
        question = db.query(Question).get(answer_data['question_id'])
        if question and answer_data['answer_text'].lower() == question.correct_answer.lower():
            answer.is_correct = True
            answer.marks_obtained = question.marks
            total_marks += question.marks
        else:
            answer.is_correct = False
            answer.marks_obtained = 0
    
    # Create test result
    test = db.query(MockTest).get(test_id)
    percentage = (total_marks / test.total_marks) * 100 if test.total_marks > 0 else 0
    
    result = TestResult(
        test_id=test_id,
        user_id=current_user.id,
        total_marks_obtained=total_marks,
        percentage=percentage,
        passed=percentage >= test.passing_marks
    )
    
    db.add(result)
    db.commit()
    
    return jsonify(result.to_dict()) 