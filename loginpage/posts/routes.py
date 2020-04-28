from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from loginpage import db
from loginpage.models import Post
from loginpage.posts.forms import PostForm, FindForm, BinsForm
from loginpage.posts.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        string = form.title.data.capitalize()
        posts = Post(title=string, content=form.content.data, bins=form.bins.data, imagen=form.picture.data, author=current_user)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            posts.imagen = picture_file
        db.session.add(posts)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/search", methods=['GET', 'POST'])
def find_post():
    form = FindForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        string = form.waste.data.capitalize()
        post = Post.query.filter_by(title=string).paginate(page=page, per_page=5)
        amount = len(post.items)
        if amount == 0:
            if current_user.is_authenticated:
                flash('Item not in list not in list, please register it on our database', 'warning')
                return redirect(url_for('posts.new_post'))
            else:
                flash('Item not in list not in list, to register it please Log in or Sign up', 'warning')
                return redirect(url_for('users.login'))
        else:
            return render_template('results.html', post=post, form=form, amount=amount, title=string)
    return render_template('find.html', form=form, title='Find')




@posts.route("/bins", methods=['GET', 'POST'])
def basura():
    form = BinsForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        string = form.bin.data
        caneca = Post.query.filter_by(bins=string).paginate(page=page, per_page=5)
        waste = len(caneca.items)
        if waste == 0:
            if current_user.is_authenticated:
                flash('There is no item in this bin, be the first to post your waste ', 'warning')
                return redirect(url_for('posts.new_post'))
            else:
                flash('There is no item in this bin. Please register'
                      ' or log in to be the first one to post your waste in this bin!', 'warning')
                return redirect(url_for('users.login'))
        else:
            return render_template('bins.html', caneca=caneca, form=form, waste=waste)
    return render_template('findbins.html', form=form, title='Bins')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.imagen = picture_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))