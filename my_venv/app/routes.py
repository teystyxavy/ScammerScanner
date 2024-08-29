from flask import Flask, Blueprint, render_template, request, jsonify, abort
import json
## from .models import MyModel

main = Blueprint('main', __name__)
DATA_FILE = 'app/data.json'

# helper function to load & save data
def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# CRUD - Create, Read, Update, Delete

# Create - Add new item
@main.route('/api/items', methods=['POST'])
def create_item():
    data = load_data()
    new_item = request.json
    new_item['id'] = max(item['id'] for item in data) + 1 if data else 1
    data.append(new_item)
    save_data(data)
    return jsonify(new_item), 201

# Read - get all items or specific item by ID
# specific item
@main.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        abort(404)
    return jsonify(item), 200

# get all items
@main.route('/api/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data), 200

# Update - update existing item by id
@main.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        abort(404)
    
    updated_item = request.json
    item.update(updated_item)
    save_data(data)
    return jsonify(item), 200

# Delete - Remove an item by ID
@main.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        abort(404)

    data.remove(item)
    save_data(data)
    return '', 204

### error 404 is not found, error 200 is OK, error 204 means OK and return nothing.