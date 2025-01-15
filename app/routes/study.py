from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models.study_material import StudyMaterial, UserProgress, Bookmark
from app.services.ai_service import analyze_content, generate_summary
import os

study_bp = Blueprint('study', __name__)

@study_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})

@study_bp.route("/materials/", methods=['POST'])
@login_required
def create_study_material():
    if not current_user.can_create_material:
        return jsonify({'error': 'Not authorized to create materials'}), 403

    # Handle file upload if provided
    file_path = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    # Analyze content if provided
    analysis = {}
    if 'content' in request.form:
        content = request.form['content']
        analysis = analyze_content(content)

    # Create study material
    db = current_app.db.session
    db_material = StudyMaterial(
        title=request.form['title'],
        content_type=request.form['content_type'],
        content=request.form['content'],
        file_path=file_path,
        **analysis
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return jsonify(db_material.to_dict())

@study_bp.route("/materials/", methods=['GET'])
@login_required
def list_study_materials():
    db = current_app.db.session
    query = db.query(StudyMaterial)
    if 'search' in request.args:
        query = query.filter(StudyMaterial.title.ilike(f"%{request.args['search']}%"))
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    materials = query.offset((page - 1) * per_page).limit(per_page).all()
    return jsonify([m.to_dict() for m in materials])

@study_bp.route("/materials/<int:material_id>/progress", methods=['GET'])
@login_required
def get_progress(material_id):
    db = current_app.db.session
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.material_id == material_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            material_id=material_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return jsonify(progress.to_dict())

@study_bp.route("/materials/<int:material_id>/bookmark", methods=['POST'])
@login_required
def toggle_bookmark(material_id):
    db = current_app.db.session
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.material_id == material_id
    ).first()
    
    if bookmark:
        db.delete(bookmark)
        db.commit()
        return jsonify({'status': 'unbookmarked'})
    
    bookmark = Bookmark(user_id=current_user.id, material_id=material_id)
    db.add(bookmark)
    db.commit()
    return jsonify({'status': 'bookmarked'}) 