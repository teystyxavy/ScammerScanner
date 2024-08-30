
-- Create the database
-- DROP DATABASE IF EXISTS database.db;
-- CREATE DATABASE ScamDetectorDB;
-- USE ScamDetectorDB;

-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Screenshots table
CREATE TABLE Screenshots (
    screenshot_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    analyzed_text TEXT,
    scam_status ENUM('RED', 'GREEN', 'YELLOW') NOT NULL,
    analysis_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Scam Templates table
CREATE TABLE ScamTemplates (
    template_id INT AUTO_INCREMENT PRIMARY KEY,
    template_text TEXT NOT NULL,
    scam_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Screenshot_Matches table
CREATE TABLE Screenshot_Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    screenshot_id INT NOT NULL,
    template_id INT NOT NULL,
    match_percentage DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (screenshot_id) REFERENCES Screenshots(screenshot_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES ScamTemplates(template_id) ON DELETE CASCADE
);

-- Create Community Posts table
CREATE TABLE CommunityPosts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    screenshot_id INT,
    content TEXT NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (screenshot_id) REFERENCES Screenshots(screenshot_id) ON DELETE SET NULL
);

-- Create Comments table
CREATE TABLE Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES CommunityPosts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Rewards table
CREATE TABLE Rewards (
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    reward_name VARCHAR(100) NOT NULL,
    points_required INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create User_Rewards table
CREATE TABLE User_Rewards (
    user_reward_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    reward_id INT NOT NULL,
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (reward_id) REFERENCES Rewards(reward_id) ON DELETE CASCADE
);

-- Insert dummy data into Users table
INSERT INTO Users (username, email, password, points)
VALUES 
('john_doe', 'john@example.com', 'password123', 100),
('jane_smith', 'jane@example.com', 'password123', 150),
('michael_brown', 'michael@example.com', 'password123', 200);

-- Insert dummy data into Screenshots table
INSERT INTO Screenshots (user_id, image_path, analyzed_text, scam_status, analysis_result)
VALUES
(1, '/path/to/screenshot1.png', 'Dear user, you have won $1,000,000. Click here to claim your prize.', 'RED', 'Suspicious links and foreign address detected.'),
(2, '/path/to/screenshot2.png', 'Your package has been shipped. Track it here.', 'GREEN', 'No suspicious elements detected.'),
(3, '/path/to/screenshot3.png', 'You are eligible for a tax refund. Provide your bank details.', 'RED', 'Foreign address and request for sensitive information detected.');

-- Insert dummy data into ScamTemplates table
INSERT INTO ScamTemplates (template_text, scam_type)
VALUES
('Dear user, you have won $1,000,000.', 'Lottery Scam'),
('You are eligible for a tax refund.', 'Phishing Scam'),
('Provide your bank details.', 'Phishing Scam');

-- Insert dummy data into Screenshot_Matches table
INSERT INTO Screenshot_Matches (screenshot_id, template_id, match_percentage)
VALUES
(1, 1, 95.00),
(3, 2, 85.00),
(3, 3, 90.00);

-- Insert dummy data into CommunityPosts table
INSERT INTO CommunityPosts (user_id, screenshot_id, content, category)
VALUES
(1, 1, 'Watch out for this scam message claiming you have won a lottery!', 'Scam Alert'),
(2, NULL, 'Is it safe to click on links in text messages from unknown numbers?', 'Discussion'),
(3, 3, 'I received a message about a tax refund. Should I be concerned?', 'Scam Alert');

-- Insert dummy data into Comments table
INSERT INTO Comments (post_id, user_id, comment_text)
VALUES
(1, 2, 'Thanks for the warning! I almost fell for it.'),
(2, 1, 'Always be cautious. Never click on links from unknown senders.'),
(3, 1, 'Yes, that sounds like a phishing attempt. Be careful.');

-- Insert dummy data into Rewards table
INSERT INTO Rewards (reward_name, points_required)
VALUES
('10% Discount Voucher', 100),
('Free Shipping Voucher', 150),
('Amazon Gift Card $10', 200);

-- Insert dummy data into User_Rewards table
INSERT INTO User_Rewards (user_id, reward_id)
VALUES
(1, 1),
(2, 2),
(3, 3);

