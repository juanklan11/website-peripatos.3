from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from loginpage import db, login_manager
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import render_template, redirect, url_for, request, flash



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


ACCESS = {'guest': 0, 'user': 1, 'admin': 2}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __str__(self):
        return "{}".format(self.username)



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))
    def __str__(self):
        return "{}".format(self.name)

    def __hash__(self):
        return hash(self.name)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __str__(self):
        return "{}".format[(self.user_id), (self.role_id)]


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(20), nullable=False, default='default_posts.jpg')
    bins = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return "{}".format(self.title)


class MyModelView(ModelView):
    can_edit = True
    can_view_details = True
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_list = ['id',
                  'name',
                  'description']
    def is_accessible(self):
        return current_user.is_authenticated

    def not_auth(self):
        return render_template('403.html')


class MyUserView(ModelView):
    can_edit = True
    can_view_details = True
    can_export = True
    export_max_rows = 1000

    export_types = ['csv', 'xls']
    column_list = ['id',
                   'username',
                   'email',
                   'image_file',
                   'roles']
    def is_accessible(self):
        if current_user.roles:
            return current_user.is_authenticated
    def not_auth(self):
        return render_template('403.html')


class MyPostView(ModelView):
    can_edit = True
    can_view_details = True
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']
    column_searchable_list = ('title',)
    column_filters = ('title', 'user_id')
    column_list = [
        'id',
        'title',
        'date_posted',
        'imagen',
        'bins',
        'author'

    ]
    def is_accessible(self):
        return current_user.is_authenticated
    def not_auth(self):
        return render_template('403.html')

class MyAdminIndexView(AdminIndexView):
    can_edit = True
    def is_accessible(self):
        if current_user.is_authenticated:
            for number in range(len(current_user.roles)):
                return current_user.roles[number].name == 'Admin'


    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash("You do not have permission to do that (403). Please check your account's credentials and try again", 'warning')
            return redirect(url_for('main.home', next=request.url))



