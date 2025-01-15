from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configure from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        # Import all models to ensure they're known to Flask-Migrate
        from app.models import User, MockTest, Question, Answer, TestResult
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
            
        # Initialize migrations after models are imported
        migrate.init_app(app, db)
        
        # Register blueprints
        from app.routes import main, auth, study, tests, resume, jobs
        app.register_blueprint(main.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(study.bp)
        app.register_blueprint(tests.bp)
        app.register_blueprint(resume.bp)
        app.register_blueprint(jobs.bp)
        
    return app

# Move user_loader to models.py to avoid circular imports 