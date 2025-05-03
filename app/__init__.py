from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devpass@localhost/medic_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '1q2w3e4r5ta'
    
    db.init_app(app)

    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from .routes.citas_routes import citas_bp
    app.register_blueprint(citas_bp)

    from .routes.pagos_routes import pagos_bp
    app.register_blueprint(pagos_bp)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
