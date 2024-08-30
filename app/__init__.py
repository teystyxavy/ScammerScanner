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

def insert_dummy_data():
    # Establish connection to SQLite database
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    # Insert data into Users table
    cur.execute('''
    INSERT INTO Users (username, email, password, points)
    VALUES 
    ('john_doe', 'john@example.com', 'password123', 100),
    ('jane_smith', 'jane@example.com', 'password123', 150),
    ('michael_brown', 'michael@example.com', 'password123', 200)
    ''')

    # Insert data into Screenshots table
    cur.execute('''
    INSERT INTO Screenshots (user_id, image_path, analyzed_text, scam_status, analysis_result)
    VALUES
    (1, '/path/to/screenshot1.png', 'Dear user, you have won $1,000,000. Click here to claim your prize.', 'RED', 'Suspicious links and foreign address detected.'),
    (2, '/path/to/screenshot2.png', 'Your package has been shipped. Track it here.', 'GREEN', 'No suspicious elements detected.'),
    (3, '/path/to/screenshot3.png', 'You are eligible for a tax refund. Provide your bank details.', 'RED', 'Foreign address and request for sensitive information detected.')
    ''')

    # Insert data into ScamTemplates table
    cur.execute('''
    INSERT INTO ScamTemplates (template_text, scam_type)
    VALUES
    ('Dear user, you have won $1,000,000.', 'Lottery Scam'),
    ('You are eligible for a tax refund.', 'Phishing Scam'),
    ('Provide your bank details.', 'Phishing Scam')
    ''')

    # Insert data into Screenshot_Matches table
    cur.execute('''
    INSERT INTO Screenshot_Matches (screenshot_id, template_id, match_percentage)
    VALUES
    (1, 1, 95.00),
    (3, 2, 85.00),
    (3, 3, 90.00)
    ''')

    # Insert data into CommunityPosts table
    cur.execute('''
    INSERT INTO CommunityPosts (user_id, screenshot_id, content, category)
    VALUES
    (1, 1, 'Watch out for this scam message claiming you have won a lottery!', 'Scam Alert'),
    (2, NULL, 'Is it safe to click on links in text messages from unknown numbers?', 'Discussion'),
    (3, 3, 'I received a message about a tax refund. Should I be concerned?', 'Scam Alert')
    ''')

    # Insert data into Comments table
    cur.execute('''
    INSERT INTO Comments (post_id, user_id, comment_text)
    VALUES
    (1, 2, 'Thanks for the warning! I almost fell for it.'),
    (2, 1, 'Always be cautious. Never click on links from unknown senders.'),
    (3, 1, 'Yes, that sounds like a phishing attempt. Be careful.')
    ''')

    # Insert data into Rewards table
    cur.execute('''
    INSERT INTO Rewards (reward_name, points_required)
    VALUES
    ('10% Discount Voucher', 100),
    ('Free Shipping Voucher', 150),
    ('Amazon Gift Card $10', 200)
    ''')

    # Insert data into User_Rewards table
    cur.execute('''
    INSERT INTO User_Rewards (user_id, reward_id)
    VALUES
    (1, 1),
    (2, 2),
    (3, 3)
    ''')

    # Commit the changes and close the connection
    con.commit()
    con.close()

def create_app():
    app = Flask(__name__)

    # Create the SQLite database and tables if they don't exist
    if not os.path.exists(DB_NAME):
        create_database()
        insert_dummy_data()
    
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
