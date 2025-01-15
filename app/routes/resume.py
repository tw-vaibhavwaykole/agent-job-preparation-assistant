from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from app.models.resume import Resume
from io import BytesIO

bp = Blueprint('resume', __name__, url_prefix='/resume')

@bp.route('/builder')
@login_required
def builder():
    return render_template('resume/builder.html')

@bp.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.get_json()
    
    # Create PDF using ReportLab
    buffer = BytesIO()
    # Add PDF generation logic here
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='resume.pdf',
        mimetype='application/pdf'
    ) 