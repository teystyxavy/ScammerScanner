import os
import sqlite3
from flask import Flask, jsonify, request
from io import BytesIO
from PIL import Image
from app.services import *
from .views import views
from .db_setup import create_database, insert_dummy_data

app = Flask(__name__)
DB_NAME = "ScamDetectorDB.db"

# route for image uploads
@app.route('/upload', methods=['POST'], strict_slashes=False)
def check_scam():
    if 'files[]' not in request.files:
        res = jsonify({
            'message' : "Nothing transmitted",
            'status' : "failed"
        })
        res.status_code = 400
        return res
    
    file = request.files.getlist('files[]')[0]
    image = Image.open(file).convert('L')

    parse_text = ParseTextService()

    text = parse_text.extract_text(image)

    first_check = ScamFirstCheckService(text=text)
    malicious = first_check.check_scam()

    res = jsonify({
        'content' : text,
        'malicious' : malicious,
        'message' : "successfully transmitted",
        'status' : "success"
    })

    return res


def create_app():
    # Create the SQLite database and tables if they don't exist
    if not os.path.exists(DB_NAME):
        create_database()
        insert_dummy_data()
    
    # Config settings
    app.config.from_pyfile('config.py')

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    app.register_blueprint(views, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
