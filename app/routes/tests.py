from flask import Blueprint, render_template
from flask_login import login_required
from app.models.mock_test import MockTest

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