import os
from flask import Flask, jsonify, request
from PIL import Image
from app.services import *
from .db_setup import create_database, insert_dummy_data
# from app.config import Config
from flask_cors import CORS

app = Flask(__name__)
DB_NAME = "ScamDetectorDB.db"
CORS(app)

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
    first_check_results = first_check.check_scam()

    second_check_results = False
    second_check_is_scam = False
    second_Check_debug = 0.0
    if first_check_results == False:
        second_check = ScamSecondCheckService()
        second_check_results = second_check.check_text(text)
        second_check_is_scam = second_check.is_scam
        second_Check_debug = second_check.highest

    


    res = jsonify({
        'content' : text,
        'first_check' : first_check_results,
        'second_check_results' : second_check_results,
        'second_check_is_scam' : second_check_is_scam,
        'message' : "successfully transmitted",
        'status' : "success",
        'score' : second_Check_debug
    })

    return res


def create_app():
    # Create the SQLite database and tables if they don't exist
    if not os.path.exists(DB_NAME):
        create_database()
        insert_dummy_data()

    from app.config import Config
    app.config.from_object(Config)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
