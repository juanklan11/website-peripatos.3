from flask import render_template, url_for, flash, redirect, request, Blueprint
from loginpage.models import Post
bins = Blueprint('bins', __name__)


@bins.route("/bins/<string:bins>")
def basura(bins):
    # page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.bins).all()
    # posts = Post.query.filter_by(bins=bins)\
    # .order_by(Post.date_posted.desc())\
    # .paginate(page=page, per_page=5)
    return render_template('bins.html', post=post, bins=bins)