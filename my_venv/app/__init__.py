from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

## db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # config settings
    app.config.from_object('config.Config')

    # Initialize extensions
    ## db.init_app(app)
    ## migrate.init_app(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app