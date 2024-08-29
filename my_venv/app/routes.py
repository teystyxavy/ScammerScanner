from flask import Blueprint, render_template, request, jsonify
## from .models import MyModel

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return 'Hello, world!'

@main.route('/api/data')
def get_data():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)

@main.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Implement logic to fetch users from the database
        pass
    elif request.method == 'POST':
        # Implement logic to create a new user in the database
        pass