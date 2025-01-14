from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_prep.db'
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import main, auth, study, tests, resume, jobs
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(study.bp)
    app.register_blueprint(tests.bp)
    app.register_blueprint(resume.bp)
    app.register_blueprint(jobs.bp)
    
    return app 