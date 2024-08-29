from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import request

app = Flask(__name__)
app.secret_key = b'\x85W\xfa,]w\xf5\xa6\xb5\xe4\xf2\x84\xb0\xcbl\x8b\xb7c\x0b\x87;\xfb,\xce'
## app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
## app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

@app.route('/items', methods=['POST'])
def create_item():
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)