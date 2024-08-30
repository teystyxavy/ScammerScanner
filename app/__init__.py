from flask import Flask
##from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .views import views
from .auth import auth
from os import path
#import sqlite3

db = SQLAlchemy()
DB_NAME = "database.db"
#con = sqlite3.connect("database.db")
#cur = con.cursor()

#cur.exectute("CREATE TABLE USER(id, password, )")
##migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # config settings
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME};'   # Initialize extensions
    db.init_app(app)
    
    ## migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Post

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')