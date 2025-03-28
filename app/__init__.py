from flask import Flask
from database import init_db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    # Import and register blueprints here
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app