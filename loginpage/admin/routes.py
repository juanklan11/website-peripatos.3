from flask import render_template, request, Blueprint, url_for, flash, redirect
from loginpage.models import Post
from loginpage.posts.forms import FindForm
from flask_login import login_user, current_user

administrador = Blueprint('admin', __name__)

# @administrador.route("/register_roles", methods=['GET', 'POST'])
# def register():
