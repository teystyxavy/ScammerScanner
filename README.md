# ScammerScanner

ScammerScanner is a web application designed to help users identify and report potential scam messages. The application allows users to upload screenshots of suspicious messages, analyze their content, and share experiences with the community. Additionally, users can earn rewards for their contributions to the platform.

## Features

### 1. User Authentication
- **Registration**: New users can register by providing a username, email, and password.
- **Login**: Registered users can log in using their credentials.
- **Profile Management**: Users can update their profile information and change their password.
- **Logout**: Users can securely log out of their accounts.

### 2. Scam Detection
- **Upload Screenshots**: Users can upload images of suspicious messages.
- **Analyze Content**: The application analyzes the uploaded screenshots and identifies potential scam indicators.
- **Scam Templates**: The system compares the text in screenshots with known scam templates to detect possible scams.

### 3. Community Forum
- **Create Posts**: Users can create new posts to share their experiences and insights about potential scams.
- **Commenting**: Users can comment on posts, providing advice or sharing similar experiences.
- **Likes**: Users can like posts to show their support.

### 4. Reward System
- **Earn Points**: Users earn points by contributing to the community (e.g., creating posts, uploading screenshots).
- **Redeem Rewards**: Points can be redeemed for various rewards, such as gift cards or vouchers.

## Technology Stack

### Backend
- **Flask**
- **SQLite**

### Frontend
- **React**
- **Tailwind CSS**

## Project Structure

```
scammerscanner/
│
├── app/
│   ├── __init__.py          # Flask application initialization
│   ├── routes.py            # API endpoints
│   ├── db_setup.py          # Database setup
│   ├── config.py            # Application configuration
│   └── services/            # Scam Detection Service Logic
│       ├── __init__.py  
│       ├── parse_text_service.py
│       ├── scam_first_check_service.py
│       ├── scam_second_check_service.py
│       └── virustotal_service.py
│
├── frontend/
│   └── react-project/
│       ├── public/
│       │   ├── rewards/     # Images for Rewards
│       │   ├── images/      # Images for Posts
│       │   └── index.html           
│       ├── src/
│       │   ├── components/          # React components (e.g., PostDetail, NewPostModal)
│       │   ├── App.js               # Main React application file
│       │   └── index.js             # React entry point
│       └── package.json             # Frontend dependencies
│
├── ScammerScannerDB.db      # SQLite Database file
├── run.py                   # Entry point to start the Flask server
└── README.md                    # Project documentation
```

## Setup and Installation

### Prerequisites
- **Python 3.x**: Required to run the Flask backend.
- **Node.js**: Required to run the React frontend.

### Backend Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/scammerscanner.git
   cd scammerscanner/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   ```bash
   python run.py
   ```

### Frontend Setup
1. **Navigate to the frontend directory**:
   ```bash
   cd frontend/react-project
   ```

2. **Install the dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```

## Usage

- **Access the application**: Once both the backend and frontend servers are running, you can access the application by navigating to `http://localhost:3000` in your web browser.
- **Register and Log In**: Create an account or log in with an existing account to start using the application.
- **Upload and Analyze Screenshots**: Go to the upload section to scan your screenshots for potential scams.
- **Participate in the Community**: Join discussions in the community forum, create new posts, comment, and like posts.
- **Earn and Redeem Rewards**: Contribute to the platform and earn points to redeem exciting rewards.

## Team
Philip, Daniel, Bryan, Xavier, Teck Ren and Denxi

---
