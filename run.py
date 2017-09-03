# Code to start application under uWSGI

from app import app
from db_alchemy import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()