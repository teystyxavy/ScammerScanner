import sqlite3

DB_NAME = "ScamDetectorDB.db"

def create_database():
    # Establish connection to SQLite database
    con = sqlite3.connect(DB_NAME)
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

    # Modified CommunityPosts table to include a title column
    cur.execute('''
    CREATE TABLE IF NOT EXISTS CommunityPosts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        screenshot_id INTEGER,
        title TEXT NOT NULL,
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
    CREATE TABLE IF NOT EXISTS Likes (
        like_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES CommunityPosts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Rewards (
        reward_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reward_name TEXT NOT NULL,
        points_required INTEGER NOT NULL,
        image_url TEXT,  -- New column for storing the image path or URL
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
    ('philiplovesLOL', 'philip.leong@gmail.com', 'iloveLOL', 1640),
    ('xavytey', 'xavier.tey@gmail.com', 'p!nk!5myf4vouritecolour', 530),
    ('jonathan_koh', 'jon.koh@gmail.com', 'iwenttoOCS', 200)
    ''')

    # Insert data into Screenshots table
    cur.execute('''
    INSERT INTO Screenshots (user_id, image_path, analyzed_text, scam_status, analysis_result)
    VALUES
    (1, '/images/lottery.png', 'Dear user, you have won $1,000,000. Click here to claim your prize.', 'RED', 'Suspicious links and foreign address detected.'),
    (2, '/images/package.jpeg', 'Your Shopee package has been shipped. Track it here.', 'GREEN', 'No suspicious elements detected.'),
    (3, '/images/iras.jpg', 'Ministry of Finance --- Dear Citizen, You are eligible for a GST refund. Provide your bank details.', 'GREEN', 'Foreign address and request for sensitive information detected.')
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
    INSERT INTO CommunityPosts (user_id, screenshot_id, title, content, category)
    VALUES
    (1, 1, 'TOTO Lottery Scam Warning', 'Watch out for this scam message claiming you have won TOTO! This kind of message is a common tactic used by scammers to lure people into giving away their personal information. They often promise a huge prize but will ask you to provide sensitive information or pay a fee to claim it. Always be skeptical of such messages, especially if they come from unknown sources.', 'Scam Alert'),
    (2, NULL, 'Suspicious UOB Bank Message', 'Is it safe to click on links in text messages from unknown numbers? I received a message that looks like it might be from UOB, but the URL is unfamiliar. I’m scared to click on it sia. I’ve heard about phishing scams. How do you verify if a link is safe?', 'Discussion'),
    (3, 3, 'GST Refund Scam Concern', 'I received a message about a GST refund. Should I be concerned? The message states that I am eligible for a GST refund and asks me to provide my bank details to process the refund. It looks legitimate, but I am wary because I know there are many scams related to taxes. Has anyone encountered something similar?', 'Scam Alert'),
    (1, NULL, 'IRAS Phone Scam', 'Received a call claiming to be from the IRAS demanding immediate payment. They said I owed back taxes and that I would be arrested if I didn’t pay right away. I’ve never heard of the IRAS operating this way, but it was very intimidating. Does anyone know if this is a known scam?', 'Scam Alert'),
    (2, 2, 'Random Shipped Shopee Package', 'Anyone got a suspicious text or email about a package delivery? I got a message this morning claiming that a package is waiting for me, but the link they provided looks real sus... It said I needed to click to arrange for redelivery or confirm my address, but I’m not expecting any packages. I think this could be a scam where they trick you into providing personal information or even install malware on your device. Be careful ah!', 'Scam Alert')
    ''')

    # Insert data into Comments table
    cur.execute('''
    INSERT INTO Comments (post_id, user_id, comment_text)
    VALUES
    (1, 2, 'Wah thanks for the warning! I almost fell for it sia :('),
    (2, 1, 'Always be cautious. Never click on links from unknown senders.'),
    (3, 1, 'Hm....')
    ''')

    # Insert data into Likes table
    cur.execute('''
    INSERT INTO Likes (post_id, user_id)
    VALUES
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 3),
    (3, 3),
    (3, 4),
    (3, 5),
    (4, 1),
    (4, 2),
    (4, 3),
    (5, 1),
    (5, 2)
    ''')

    # Insert data into Rewards table
    cur.execute('''
    INSERT INTO Rewards (reward_name, points_required, image_url)
    VALUES
    ('NTUC $5 Voucher', 100, '/rewards/ntuc.png'),
    ('NTUC $10 Voucher', 275, '/rewards/ntuc.png'),
    ('Amazon Gift Card $10', 250, '/rewards/amazon.jpeg'),
    ('Starbucks Gift Card $5', 100, '/rewards/starbucks.jpeg'),
    ('Apple Music 1 Month', 250, '/rewards/applemusic.png'),
    ('Google Play Gift Card $10', 200, '/rewards/google.png'),
    ('Netflix Gift Card $20', 400, '/rewards/netflix.jpeg'),
    ('Spotify Premium 1 Month', 250, '/rewards/spotify.png'),
    ('Grab Voucher $5', 100, '/rewards/grab.png'),
    ('H&M Gift Card $25', 500, '/rewards/hm.jpeg')
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
