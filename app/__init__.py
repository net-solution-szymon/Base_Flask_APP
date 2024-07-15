from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


import json

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
mail = Mail()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    
    
    # app.config.from_file("../pconfig.json", load=json.load)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)


    from .models import User

    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

   

    #inicjalizajca bazy danych:
    with app.app_context():
        db.create_all()

    
    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)
    

    return app

