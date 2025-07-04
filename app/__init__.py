from flask import Flask
from app.webhook.routes import bp
import os

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_path = os.path.join(base_dir, '..', 'templates')
    
    app = Flask(__name__, template_folder=templates_path)
    app.register_blueprint(bp)
    return app
