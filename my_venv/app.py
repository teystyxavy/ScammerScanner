from flask import Flask, jsonify, request, session, make_response
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import request\

app = Flask(__name__)
app.secret_key = b'\x85W\xfa,]w\xf5\xa6\xb5\xe4\xf2\x84\xb0\xcbl\x8b\xb7c\x0b\x87;\xfb,\xce'
## app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
## app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Implement logic to fetch users from the database
        pass
    elif request.method == 'POST':
        # Implement logic to create a new user in the database
        pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)