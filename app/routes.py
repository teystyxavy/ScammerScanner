from flask import Flask, Blueprint, render_template, request, jsonify, abort
import json
import sqlite3
## from .models import MyModel

main = Blueprint('main', __name__)
DATA_FILE = 'app/data.json'

DB_NAME = "ScamDetectorDB.db"
# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This allows fetching rows as dictionaries
    return conn

# helper function to load & save data
def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# CRUD - Create, Read, Update, Delete

# Create - Add new community post
@main.route('/api/posts', methods=['POST'])
def create_post():
    conn = get_db_connection()
    cur = conn.cursor()
    
    new_post = request.json
    cur.execute('''
        INSERT INTO CommunityPosts (user_id, screenshot_id, content, category)
        VALUES (?, ?, ?, ?)
    ''', (new_post['user_id'], new_post.get('screenshot_id'), new_post['content'], new_post['category']))
    
    conn.commit()
    new_post_id = cur.lastrowid
    conn.close()

    new_post['post_id'] = new_post_id
    return jsonify(new_post), 201

@main.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the specific community post by ID, including the title
    cur.execute('SELECT * FROM CommunityPosts WHERE post_id = ?', (post_id,))
    post = cur.fetchone()
    
    if post is None:
        conn.close()
        abort(404)
    
    # Fetch the associated user details
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (post['user_id'],))
    user = cur.fetchone()

    # Fetch the associated screenshot details if available
    screenshot = None
    if post['screenshot_id'] is not None:
        cur.execute('SELECT * FROM Screenshots WHERE screenshot_id = ?', (post['screenshot_id'],))
        screenshot = cur.fetchone()

    conn.close()

    # Convert rows to dictionaries
    post_dict = {
        "post_id": post["post_id"],
        "title": post["title"],  # Include the title
        "content": post["content"],
        "category": post["category"],
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]
    }
    user_dict = dict(user) if user else None
    screenshot_dict = dict(screenshot) if screenshot else None

    # Include user and screenshot details in the response
    response = {
        'post': post_dict,
        'user': user_dict,
        'screenshot': screenshot_dict
    }

    return jsonify(response), 200



@main.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch all community posts with associated user and screenshot details, including the title
    cur.execute('''
        SELECT 
            p.post_id, p.title, p.content, p.category, p.created_at, p.updated_at, 
            u.user_id, u.username, u.email, u.points, 
            s.screenshot_id, s.image_path, s.analyzed_text, s.scam_status, s.analysis_result
        FROM 
            CommunityPosts p
        JOIN 
            Users u ON p.user_id = u.user_id
        LEFT JOIN 
            Screenshots s ON p.screenshot_id = s.screenshot_id
    ''')
    
    posts = cur.fetchall()
    conn.close()

    # Process the data to include user and screenshot details in the response
    results = []
    for post in posts:
        post_dict = {
            "post": {
                "post_id": post["post_id"],
                "title": post["title"],  # Include the title
                "content": post["content"],
                "category": post["category"],
                "created_at": post["created_at"],
                "updated_at": post["updated_at"]
            },
            "user": {
                "user_id": post["user_id"],
                "username": post["username"],
                "email": post["email"],
                "points": post["points"]
            },
            "screenshot": {
                "screenshot_id": post["screenshot_id"],
                "image_path": post["image_path"],
                "analyzed_text": post["analyzed_text"],
                "scam_status": post["scam_status"],
                "analysis_result": post["analysis_result"]
            } if post["screenshot_id"] else None
        }
        results.append(post_dict)

    return jsonify(results), 200



# Update - Update existing community post by ID
@main.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM CommunityPosts WHERE post_id = ?', (post_id,))
    post = cur.fetchone()
    
    if post is None:
        conn.close()
        abort(404)
    
    updated_post = request.json
    cur.execute('''
        UPDATE CommunityPosts SET user_id = ?, screenshot_id = ?, content = ?, category = ?, updated_at = CURRENT_TIMESTAMP
        WHERE post_id = ?
    ''', (updated_post['user_id'], updated_post.get('screenshot_id'), updated_post['content'], updated_post['category'], post_id))
    
    conn.commit()
    conn.close()
    
    updated_post['post_id'] = post_id
    return jsonify(updated_post), 200

# Delete - Remove a community post by ID
@main.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM CommunityPosts WHERE post_id = ?', (post_id,))
    post = cur.fetchone()
    
    if post is None:
        conn.close()
        abort(404)
    
    cur.execute('DELETE FROM CommunityPosts WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    return '', 204


# Get - Get a user details for profile page
@main.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT username, email, points, created_at, updated_at FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()

    if user is None:
        conn.close()
        abort(404)

    # put user details from row into dict
    user_dict = {
        "username": user["username"],
        "email": user["email"],
        "points": user["points"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

    return jsonify(user_dict), 200

# Update - Update a user details for profile page
# updates username, eail and updated_at for specific user_id
# doesn't update points, password & created_at
@main.route('/api/user/<int:user_id>', methods=['PUT'])
def update_userDetails(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT username, email, updated_at FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    
    if user is None:
        conn.close()
        abort(404)
    
    updated_user = request.json
    cur.execute('''
        UPDATE Users SET username = ?, email = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (updated_user['username'], updated_user('email'), updated_user('user_id')))
    
    conn.commit()
    conn.close()
    
    updated_user['user_id'] = user_id
    return jsonify(updated_user), 200

# Update - Update a user's password
@main.route('/api/password/<int:user_id>', methods=['PUT'])
def update_userPassword(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT password, updated_at FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    
    if user is None:
        conn.close()
        abort(404)
    
    updated_user = request.json
    cur.execute('''
        UPDATE Users SET password = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (updated_user['password'], updated_user('user_id')))
    
    conn.commit()
    conn.close()
    
    updated_user['user_id'] = user_id
    return jsonify(updated_user), 200


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

