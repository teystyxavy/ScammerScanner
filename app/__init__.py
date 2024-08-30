from flask import Flask
##from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .views import views
from .auth import auth
from os import path
import sqlite3
from sqlalchemy import create_engine, text
# cur = con.cursor()

#cur.execute("CREATE TABLE USER(id, password, )")
##migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    #create sqlite db
    con = sqlite3.connect(DB_NAME)
    
    # config settings
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'   # Initialize extensions
    db = SQLAlchemy(app)
    engine = test_connection()
    ## migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def test_connection():
    engine = create_engine(f'sqlite:///{DB_NAME}')

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection is successful. Result:", result.fetchone())

            with open('C:/MY OWN PROJECTS/.hack_hackathon/ScammmerScanner/app/Database-Setup.sql') as file:
                query = text(file.read())
                connection.execute(text("CREATE TABLE Users(user_id INT PRIMARY KEY,username VARCHAR(50));"))
                connection.execute(text("INSERT INTO Users VALUES (300, 'john_doe'),(212, 'jane_smith'),(121, 'michael_brown');"))
                result = connection.execute(text("Select * from users;"))
                for row in result:
                    print(row)

    except Exception as e:
        print("Connection failed:", e)

    return engine
    