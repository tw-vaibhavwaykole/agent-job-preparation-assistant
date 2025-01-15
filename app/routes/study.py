from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from app.models.study_material import StudyMaterial

bp = Blueprint('study', __name__, url_prefix='/study')

@bp.route('/')
@login_required
def list_study_materials():
    try:
        materials = StudyMaterial.query.all()
        return render_template('study/list.html', materials=materials)
    except Exception as e:
        flash('Error loading study materials')
        return redirect(url_for('main.dashboard'))

@bp.route('/<int:id>')
@login_required
def view_material(id):
    material = StudyMaterial.query.get_or_404(id)
    return render_template('study/view.html', material=material) 