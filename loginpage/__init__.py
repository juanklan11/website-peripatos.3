from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from loginpage.config import Config
from flask_admin import Admin
from tablib import  *
from flask_user import UserManager
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual

from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_appbuilder import SQLA, AppBuilder




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
# admin = Admin(template_mode='bootstrap3')
admin = Admin(name='Dashboard')
# user_manager = UserManager()
# security = Security()
# appbuilder = AppBuilder()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    from loginpage.models import User, Post, Role, db, MyModelView, MyPostView, MyUserView, MyAdminIndexView
    db.init_app(app)
    with app.app_context():
        db.create_all()



    admin.init_app(app, index_view=MyAdminIndexView())

    # admin.add_view(ContactModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyUserView(User, db.session))
        # admin.add_view(TreeView(User, db.session))
    admin.add_view(MyPostView(Post, db.session))
        # admin.add_view(TreeView(Tree, db.session, category="Other"))
    admin.add_sub_category(name="Links", parent_name="Other")

    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    # user_manager.init_app(app, db, User)
    mail.init_app(app)
    # security.init_app(app, user_datastore)


    from loginpage.users.routes import users
    from loginpage.posts.routes import posts
    from loginpage.main.routes import main
    from loginpage.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)


    return app

