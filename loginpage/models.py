from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from loginpage import db, login_manager
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, BaseView
from flask_security import Security, SQLAlchemyUserDatastore
from flask import render_template, redirect, url_for, request, flash
from tablib import  *
# from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_table import Table, Col


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


    # def is_admin(self):
    #     return self.access == ACCESS['admin']
    #
    # def allowed(self, access_level):
    #     return self.access >= access_level

    def __str__(self):
        return "{}".format(self.username)

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.roles}')"


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
    # featured_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    # featured_post = db.relationship('Post', foreign_keys=[featured_post_id])
    def __str__(self):
        return "{}".format(self.title)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}',{self.imagen})"

# class Tree(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#
#     # recursive relationship
#     parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
#     parent = db.relationship('Tree', remote_side=[id], backref='children')
#
#     def __str__(self):
#         return "{}".format(self.name)


# class TreeView(ModelView):
#     list_template = 'tree_list.html'
#     column_auto_select_related = True
#     column_list = [
#         'username',
#         'email',
#             ]
#
#     column_filters = ['id', 'username', 'email', ]
#
#     # override the 'render' method to pass your own parameters to the template
#     def render(self, template, **kwargs):
#         return super(TreeView, self).render(template, foo="bar", **kwargs)



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
        # return current_user.is_authenticated
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
        # return current_user.is_authenticated and current_user.username == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash("You do not have permission to do that (403). Please check your account's credentials and try again", 'warning')
            return redirect(url_for('main.home', next=request.url))
        # return current_user.is_authenticated

    # def __init__(self, *args, **kwargs):
    #     self.roles_accepted = kwargs.pop('roles_accepted', list())
    #     super(MyAdminIndexView, self).__init__(*args, **kwargs)

# class GroupModelView(ModelView):
#     datamodel = SQLAInterface(User)




# class MyAdminIndexView(AdminIndexView):
#     can_edit = True
#     def is_accessible(self):
#         return current_user.is_authenticated

# class ContactModelView(ModelView):
#     datamodel = SQLAInterface(User)




