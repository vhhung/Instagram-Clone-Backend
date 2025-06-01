import os
from flask import Flask, request, Response, make_response
from prometheus_client import Counter, Gauge, Histogram, Summary, make_wsgi_app, REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

#Initialize extensions
jwt = JWTManager()
db = SQLAlchemy()
UPLOAD_FOLDER = 'uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
ABSOLUTE_UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)

REQUEST_COUNT = Counter(
    'tralalero_tralala_http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint']
)

POSTS_CREATED = Counter(
    'tralalero_tralala_posts_created_total',
    'Number of posts created'
)

REQUEST_LATENCY = Histogram(
    'tralalero_tralala_http_request_duration_seconds',
    'HTTP Request latency',
    ['method', 'endpoint']
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'viethungt1k30cht'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    jwt.init_app(app)
    db.init_app(app)

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(request, 'endpoint') and request.endpoint != 'static' and request.endpoint != 'prometheus':
            latency = time.time() - request.start_time
            REQUEST_LATENCY.labels(method=request.method, endpoint=request.endpoint).observe(latency)
            REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
        return response


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

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app(REGISTRY)
    })

    @app.route('/uploads/<filename>')
    def upload_file(filename):
        return send_from_directory(ASOLUTE_UPLOAD_FOLDER, filename)

    if not os.path.exists(ABSOLUTE_UPLOAD_FOLDER):
        os.makedirs(ABSOLUTE_UPLOAD_FOLDER)    

    return app