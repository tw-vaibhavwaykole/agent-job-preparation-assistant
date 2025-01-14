from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from openai import OpenAI
import os

bp = Blueprint('jobs', __name__, url_prefix='/jobs')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@bp.route('/recommendations')
@login_required
def recommendations():
    # Placeholder for job recommendations
    sample_jobs = [
        {
            'title': 'Software Engineer',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'salary': '$120,000 - $150,000'
        },
        {
            'title': 'Data Scientist',
            'company': 'AI Solutions',
            'location': 'New York, NY',
            'salary': '$130,000 - $160,000'
        }
    ]
    return render_template('jobs/recommendations.html', jobs=sample_jobs)

@bp.route('/ai-tips')
@login_required
def ai_tips():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional career advisor helping with job interview preparation."
                },
                {
                    "role": "user",
                    "content": f"Generate professional interview tips for a {current_user.interests} position. Include common questions and best practices."
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return jsonify({'tips': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 