from app import flask_app
from flask import render_template


@flask_app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')