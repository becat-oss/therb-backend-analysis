from flask import Flask
from src.database import init_db
import src.models

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')
    init_db(app)

    return app

app=create_app()

