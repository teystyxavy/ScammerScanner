import os
from flask import Flask
from .views import views
from .db_setup import create_database, insert_dummy_data
from config import Config


DB_NAME = "ScamDetectorDB.db"

def create_app():
    app = Flask(__name__)

    # Create the SQLite database and tables if they don't exist
    if not os.path.exists(DB_NAME):
        create_database()
        insert_dummy_data()
    
    # Config settings
    app.config.from_object(Config)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    app.register_blueprint(views, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
