from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Development
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True)
    # Production
    else:
        app.run(host='0.0.0.0', port=5000) 