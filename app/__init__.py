import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

#Initialize extensions
jwt = JWTManager()
db = SQLAlchemy()
UPLOAD_FOLDER = 'uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
ABSOLUTE_UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'viethungt1k30cht'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    jwt.init_app(app)
    db.init_app(app)

    # Import and register blueprint
    from app.controllers.auth import auth_bp
    from app.controllers.user import user_bp
    from app.controllers.upload import upload_bp
    from app.controllers.post import post_bp
    from app.controllers.follow import follow_bp
    from app.controllers.like import like_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(post_bp, url_prefix='/api/post')
    app.register_blueprint(follow_bp, url_prefix='/api/follow')
    app.register_blueprint(like_bp, url_prefix='/api/like')

    @app.route('/uploads/<filename>')
    def upload_file(filename):
        return send_from_directory(ASOLUTE_UPLOAD_FOLDER, filename)

    if not os.path.exists(ABSOLUTE_UPLOAD_FOLDER):
        os.makedirs(ABSOLUTE_UPLOAD_FOLDER)    

    return app