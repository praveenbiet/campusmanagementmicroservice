from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from people.routes import people_bp
    from academic.routes import academic_bp
    from student_records.routes import student_records_bp
    # Add other blueprints as they are created
    
    app.register_blueprint(people_bp, url_prefix='/api/v1/people')
    app.register_blueprint(academic_bp, url_prefix='/api/v1/academic')
    app.register_blueprint(student_records_bp, url_prefix='/api/v1/student-records')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500
    
    return app 