from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import StudyMaterial
from app import db

bp = Blueprint('study', __name__, url_prefix='/study')

@bp.route('/materials')
@login_required
def materials():
    categories = ['Competitive Exams', 'Government Jobs', 'Private Sector']
    materials = StudyMaterial.query.all()
    return render_template('study/materials.html', materials=materials, categories=categories)

@bp.route('/materials/<int:id>')
@login_required
def material_detail(id):
    material = StudyMaterial.query.get_or_404(id)
    return render_template('study/detail.html', material=material)

@bp.route('/materials/add', methods=['GET', 'POST'])
@login_required
def add_material():
    if request.method == 'POST':
        material = StudyMaterial(
            title=request.form['title'],
            category=request.form['category'],
            content=request.form['content'],
            external_link=request.form['external_link']
        )
        db.session.add(material)
        db.session.commit()
        flash('Study material added successfully!')
        return redirect(url_for('study.materials'))
    return render_template('study/add.html') 