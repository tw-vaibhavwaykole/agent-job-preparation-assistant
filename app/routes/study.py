from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import StudyMaterial
from app import db
from app.utils.file_handler import FileHandler
from app.utils.ai_content_analyzer import AIContentAnalyzer

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

@bp.route('/materials/upload', methods=['POST'])
@login_required
def upload_material():
    try:
        file = request.files['file']
        content = request.form.get('content')
        title = request.form.get('title')
        
        # Save file if provided
        file_path = None
        if file:
            file_path = FileHandler.save_file(file)
        
        # Analyze content with AI
        ai_analyzer = AIContentAnalyzer()
        analysis = ai_analyzer.analyze_content(content or file_path, 
                                            content_type=file.content_type if file else 'text')
        
        # Create study material
        material = StudyMaterial(
            title=title,
            content=content,
            file_path=file_path,
            ai_summary=analysis.get('summary'),
            keywords=analysis.get('keywords'),
            difficulty_level=analysis.get('difficulty_level'),
            estimated_time=analysis.get('estimated_time')
        )
        
        db.session.add(material)
        db.session.commit()
        
        return jsonify({"success": True, "material_id": material.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/materials/search', methods=['GET'])
@login_required
def search_materials():
    query = request.args.get('q', '')
    try:
        # AI-powered search
        ai_analyzer = AIContentAnalyzer()
        search_results = ai_analyzer.search_materials(query)
        return jsonify(search_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 