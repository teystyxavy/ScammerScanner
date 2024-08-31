from flask import Blueprint, request, jsonify, session, abort
import json
import sqlite3
from werkzeug.utils import secure_filename
import os
## from .models import MyModel

main = Blueprint('main', __name__)
DATA_FILE = 'app/data.json'

DB_NAME = "ScamDetectorDB.db"
# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This allows fetching rows as dictionaries
    return conn

# Set definitions for File Upload
# Assuming your routes.py is inside the `app` directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Define the relative path from `app` directory to the upload folder
UPLOAD_FOLDER = os.path.join(basedir, '../frontend/react-project/public/images')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CRUD - Create, Read, Update, Delete
# Create - Add new community post
@main.route('/api/posts', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    title = request.form.get('title')
    content = request.form.get('content')

    # Check if the post data is valid
    if not content:
        return jsonify({"error": "Content is required"}), 400

    screenshot_id = None
    if 'screenshot' in request.files:
        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            relative_path = f'/images/{filename}'

            conn = get_db_connection()
            cur = conn.cursor()
            
            # Insert the screenshot into the Screenshots table along with user_id
            cur.execute('''
                INSERT INTO Screenshots (user_id, image_path, scam_status)
                VALUES (?, ?, ?)
            ''', (user_id, relative_path, 'RED'))
            
            conn.commit()
            screenshot_id = cur.lastrowid
            conn.close()

    # Insert the post into the CommunityPosts table
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO CommunityPosts (user_id, screenshot_id, content, title, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, screenshot_id, content, title, 'Discussion'))

    conn.commit()
    new_post_id = cur.lastrowid
    conn.close()

    new_post = {
        'post_id': new_post_id,
        'user_id': user_id,
        'content': content,
        'screenshot_id': screenshot_id
    }

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
from flask import request, jsonify, abort, session

@main.route('/api/user/<int:user_id>', methods=['PUT'])
def update_userDetails(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the current user details
    cur.execute('SELECT username, email, password FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()

    if user is None:
        conn.close()
        abort(404)

    updated_user = request.json
    current_password = updated_user.get('currentPassword')

    # Validate the current password
    if not current_password or current_password != user['password']:
        conn.close()
        return jsonify({"error": "Incorrect password"}), 403

    # Update the user details
    cur.execute('''
        UPDATE Users SET username = ?, email = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (updated_user['username'], updated_user['email'], user_id))
    
    conn.commit()
    conn.close()

    # Return the updated user details (excluding password)
    updated_user = {
        'user_id': user_id,
        'username': updated_user['username'],
        'email': updated_user['email']
    }
    return jsonify(updated_user), 200


# Update - Update a user's password
@main.route('/api/password', methods=['PUT'])
def update_userPassword():
    # Get the current user_id from the session
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch the current password from the database
    cur.execute('SELECT password FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    
    if user is None:
        conn.close()
        abort(404)
    
    # Extract the current password and new password from the request
    updated_user = request.json
    current_password = updated_user.get('currentPassword')
    new_password = updated_user.get('newPassword')
    
    # Validate the current password
    if user['password'] != current_password:
        conn.close()
        return jsonify({"error": "Current password is incorrect"}), 403
    
    # Update the password with the new password
    cur.execute('''
        UPDATE Users SET password = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (new_password, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Password updated successfully"}), 200

# Register endpoint
@main.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Please provide username, email, and password"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the username or email already exists
    cur.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (username, email))
    existing_user = cur.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 400

    # Insert the new user into the database without hashing the password
    cur.execute('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)', 
                (username, email, password))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()

    session['user_id'] = user_id
    session['username'] = username

    return jsonify({"message": "User registered successfully"}), 201

# Login endpoint
@main.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Please provide username and password"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Find the user by username
    cur.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cur.fetchone()
    conn.close()

    if not user or user['password'] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # If the user is authenticated, start a session
    session['user_id'] = user['user_id']
    session['username'] = user['username']

    return jsonify({"message": "Logged in successfully"}), 200

# Logout endpoint
@main.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Get current user
@main.route('/api/current_user', methods=['GET'])
def current_user():
    if 'user_id' in session:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch the user data from the database using the session user_id
        cur.execute('SELECT * FROM Users WHERE user_id = ?', (session['user_id'],))
        user = cur.fetchone()
        conn.close()

        if user:
            return jsonify({
                "user_id": user['user_id'],
                "username": user['username'],
                "email": user['email']
            }), 200
    
    return jsonify({"error": "Not logged in"}), 401

# Get Rewards
@main.route('/api/rewards', methods=['GET'])
def get_rewards():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch and sort rewards based on points_required in ascending order
    cur.execute('SELECT * FROM Rewards ORDER BY points_required ASC')
    rewards = cur.fetchall()

    conn.close()

    # Convert to dictionary format
    rewards_list = []
    for reward in rewards:
        rewards_list.append({
            "reward_id": reward["reward_id"],
            "reward_name": reward["reward_name"],
            "points_required": reward["points_required"],
            "image_url": reward["image_url"]
        })

    return jsonify(rewards_list), 200

# Claim Reward
@main.route('/api/claim_reward', methods=['POST'])
def claim_reward():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']
    reward_id = request.json.get('reward_id')

    if not reward_id:
        return jsonify({"error": "Reward ID is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Get the user's points
    cur.execute('SELECT points FROM Users WHERE user_id = ?', (user_id,))
    user = cur.fetchone()

    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    user_points = user['points']

    # Get the reward details
    cur.execute('SELECT points_required FROM Rewards WHERE reward_id = ?', (reward_id,))
    reward = cur.fetchone()

    if not reward:
        conn.close()
        return jsonify({"error": "Reward not found"}), 404

    points_required = reward['points_required']

    if user_points < points_required:
        conn.close()
        return jsonify({"error": "Not enough points to claim this reward"}), 400

    # Deduct points from the user
    cur.execute('UPDATE Users SET points = points - ? WHERE user_id = ?', (points_required, user_id))

    # Record the claimed reward
    cur.execute('INSERT INTO User_Rewards (user_id, reward_id) VALUES (?, ?)', (user_id, reward_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Reward claimed successfully"}), 200

# Toggle Like in a Post
@main.route('/api/posts/<int:post_id>/toggle_like', methods=['POST'])
def toggle_like(post_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the user has already liked the post
    cur.execute('''
        SELECT * FROM Likes WHERE post_id = ? AND user_id = ?
    ''', (post_id, user_id))
    existing_like = cur.fetchone()

    if existing_like:
        # If the user has already liked the post, remove the like
        cur.execute('''
            DELETE FROM Likes WHERE post_id = ? AND user_id = ?
        ''', (post_id, user_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Like removed"}), 200
    else:
        # If the user hasn't liked the post, add the like
        cur.execute('''
            INSERT INTO Likes (post_id, user_id) VALUES (?, ?)
        ''', (post_id, user_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Post liked"}), 201

# Get Total Likes of a Post and if Post is liked by user
@main.route('/api/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    
    conn = get_db_connection()
    cur = conn.cursor()

    # Query to count the number of likes for the specified post
    cur.execute('''
        SELECT COUNT(*) as likes_count FROM Likes WHERE post_id = ?
    ''', (post_id,))
    result = cur.fetchone()

    # Query to check if the current user has liked the post
    cur.execute('''
        SELECT EXISTS(SELECT 1 FROM Likes WHERE post_id = ? AND user_id = ?) as is_liked
    ''', (post_id, user_id))
    user_liked = cur.fetchone()

    conn.close()

    if result:
        return jsonify({
            "post_id": post_id,
            "likes_count": result['likes_count'],
            "isLiked": bool(user_liked['is_liked'])  # Convert to boolean (will be False if user_liked['is_liked'] is 0)
        }), 200
    else:
        return jsonify({"error": "Post not found"}), 404

# Get all Comments of a Post
@main.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT Comments.comment_id, Comments.comment_text, Comments.created_at, 
               Users.user_id, Users.username
        FROM Comments
        JOIN Users ON Comments.user_id = Users.user_id
        WHERE Comments.post_id = ?
        ORDER BY Comments.created_at ASC
    ''', (post_id,))
    
    comments = cur.fetchall()
    conn.close()

    if comments:
        comments_list = []
        for comment in comments:
            comments_list.append({
                "comment_id": comment['comment_id'],
                "comment_text": comment['comment_text'],
                "created_at": comment['created_at'],
                "user_id": comment['user_id'],
                "username": comment['username']
            })

        return jsonify({"post_id": post_id, "comments": comments_list}), 200
    else:
        return jsonify({"error": "No comments found for this post"}), 404

# Create new Comment
@main.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    comment_text = request.json.get('comment_text')

    # Check if the comment text is provided
    if not comment_text:
        return jsonify({"error": "Comment text is required"}), 400

    # Insert the new comment into the Comments table
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Comments (post_id, user_id, comment_text)
        VALUES (?, ?, ?)
    ''', (post_id, user_id, comment_text))
    
    conn.commit()
    new_comment_id = cur.lastrowid

    cur.execute('''
        SELECT username FROM Users WHERE user_id = ?
    ''', (user_id,))
    user = cur.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    new_comment = {
        "comment_id": new_comment_id,
        "post_id": post_id,
        "user_id": user_id,
        "username": user['username'],
        "comment_text": comment_text
    }

    return jsonify(new_comment), 201

