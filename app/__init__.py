import os
import sqlite3
from flask import Flask
from .views import views
from .auth import auth

DB_NAME = "ScamDetectorDB.db"

def create_database():
    # Establish connection to SQLite database
    con = sqlite3.connect(DB_NAME)
    
    # Create a cursor object using the connection
    cur = con.cursor()
    
    # Execute SQL statements to create tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        points INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Screenshots (
        screenshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        analyzed_text TEXT,
        scam_status TEXT CHECK(scam_status IN ('RED', 'GREEN', 'YELLOW')) NOT NULL,
        analysis_result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ScamTemplates (
        template_id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_text TEXT NOT NULL,
        scam_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Screenshot_Matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        screenshot_id INTEGER NOT NULL,
        template_id INTEGER NOT NULL,
        match_percentage REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (screenshot_id) REFERENCES Screenshots(screenshot_id) ON DELETE CASCADE,
        FOREIGN KEY (template_id) REFERENCES ScamTemplates(template_id) ON DELETE CASCADE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS CommunityPosts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        screenshot_id INTEGER,
        content TEXT NOT NULL,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (screenshot_id) REFERENCES Screenshots(screenshot_id) ON DELETE SET NULL
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES CommunityPosts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Rewards (
        reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reward_name TEXT NOT NULL,
        points_required INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS User_Rewards (
        user_reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reward_id INTEGER NOT NULL,
        claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (reward_id) REFERENCES Rewards(reward_id) ON DELETE CASCADE
    )
    ''')

    # Commit the changes and close the connection
    con.commit()
    con.close()

def create_app():
    app = Flask(__name__)

    # Create the SQLite database and tables if they don't exist
    if not os.path.exists(DB_NAME):
        create_database()
    
    # Config settings
    app.config.from_object('config.Config')

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
