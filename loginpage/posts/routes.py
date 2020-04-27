from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from loginpage import db
from loginpage.models import Post, Role, User
from loginpage.posts.forms import PostForm, FindForm, BinsForm
from loginpage.posts.utils import save_picture
from werkzeug.utils import secure_filename
from flask_user import roles_required




posts = Blueprint('posts', __name__)

# @posts.route('/post/new',methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             post.imagen = picture_file
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('users.account'))
#     return render_template('create_post.html', title='Create post', form=form)


# @posts.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             post.imagen = picture_file
#         db.session.add(picture_file)
#         db.session.add(Post.title)
#         db.session.add(Post.content)
#         db.session.commit()
#         flash('Your post was created!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_post.html', title='New Post',form=form, legend='New Post')

# @posts.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         posts = Post(title=form.title.data, content=form.content.data, author=current_user, imagen=form.picture.data)
#         db.session.add(posts)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_post.html', title='New Post',
#                            form=form, legend='New Post')


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

# @posts.route("/post/find", methods=['GET', 'POST'])
# def find_post():
#     form = FindForm()
#     if form.validate_on_submit():
#         page = request.args.get('page', 1, type=int)
#         string = form.waste.data.capitalize()
#         post = Post.query.filter_by(title=string).paginate(page=page, per_page=5)
#         amount = len(post.items)
#         if amount == 0:
#             if current_user.is_authenticated:
#                 flash('Item not in list not in list, please register it on our database', 'warning')
#                 return redirect(url_for('posts.new_post'))
#             else:
#                 flash('Item not in list not in list, to register it please Log in or Sign up', 'warning')
#                 return redirect(url_for('users.login'))
#         else:
#             return render_template('results.html', post=post, form=form, amount=amount, title=string)
#     return render_template('find.html', form=form, title='Find')

# CORRECT AS OF 26.04.20 17.53PM
# @posts.route("/post/find", methods=['GET', 'POST'])
# def find_post():
#     form = FindForm()
#     if form.validate_on_submit():
#         # page = request.args.get('page', 1, type=int)
#         string = form.waste.data.capitalize()
#         post = Post.query.filter_by(title=string).first()
#         if post is None:
#             if current_user.is_authenticated:
#                 flash('Item not in list not in list, please register it on our database', 'warning')
#                 return redirect(url_for('posts.new_post'))
#             else:
#                 flash('Item not in list not in list, to register it please Log in or Sign up', 'warning')
#                 return redirect(url_for('users.login'))
#         else:
#             return render_template('results.html', post=post, form=form)
#     return render_template('find.html', form=form, title='Find')


# @posts.route("/post/find", methods=['GET', 'POST'])
# def find_post():
#     form = FindForm()
#     if form.validate_on_submit():
#         page = request.args.get('page', 1, type=int)
#         string = form.waste.data.capitalize()
#         post = Post.query.filter_by(title=string).paginate(page=page, per_page=5)
#         waste = len(post.items)
#         if post is None:
#             if current_user.is_authenticated:
#                 flash('Item not in list not in list, please register it on our database', 'warning')
#                 return redirect(url_for('posts.new_post'))
#             else:
#                 flash('Item not in list not in list, to register it please Log in or Sign up', 'warning')
#                 return redirect(url_for('users.login'))
#         else:
#             return render_template('results.html', post=post, form=form, waste=waste)
#     return render_template('find.html', form=form, title='Find')

#
# @posts.route("/post/find", methods=['GET', 'POST'])
# def find_post():
#     form = FindForm()
#     if form.validate_on_submit():
#         page = request.args.get('page', 1, type=int)
#         string = form.waste.data
#         desecho = Post.query.filter_by(title=string).paginate(page=page, per_page=5)
#         num = len(desecho.items)
#         if num == 0:
#             if current_user.is_authenticated:
#                 flash('Item not in list not in list, please register it on our database', 'warning')
#                 return redirect(url_for('posts.new_post'))
#             else:
#                 flash('Item not in list not in list, to register it please Log in or Sign up', 'warning')
#                 return redirect(url_for('users.login'))
#         else:
#             return render_template('results.html', desecho=desecho, form=form, num=num)
#     return render_template('find.html', form=form, title='Find')


# @posts.route("/bins", methods=['GET', 'POST'])
# def basura():
#     form = FindForm()
#     if form.validate_on_submit():
#         page = request.args.get('page', 1, type=int)
#         string = form.waste.data
#         caneca = Post.query.filter_by(title=string).paginate(page=page, per_page=5)
#         desecho = len(caneca.items)
#         if desecho == 0:
#             if current_user.is_authenticated:
#                 flash('There is no item in this bin, be the first to post your waste ', 'warning')
#                 return redirect(url_for('posts.new_post'))
#             else:
#                 flash('There is no item in this bin. Please register'
#                       ' or log in to be the first one to post your waste in this bin!', 'warning')
#                 return redirect(url_for('users.login'))
#         else:
#             return render_template('bins.html', caneca=caneca, form=form, desecho=desecho)
#     # page = request.args.get('page', 1, type=int)
#     # # exist = Post.query.get_or_404(bins)
#     # caneca = Post.query.filter_by(bins=).paginate(page=page, per_page=5)
#     # waste = len(caneca.items)
#     # # post = Post.query.filter_by(bins=bins).first_or_404()
#     # # posts = Post.query.filter_by(bins=bins)\
#     # # .order_by(Post.date_posted.desc())\
#     # # .paginate(page=page, per_page=5)
#     return render_template('findbins.html', form=form, title='Bins')


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

# @posts.route("/bins/<string:bins>", methods=['GET', 'POST'])
# def basura(bins):
#     form = FindForm()
#     page = request.args.get('page', 1, type=int)
#     # exist = Post.query.get_or_404(bins)
#     caneca = Post.query.filter_by(bins=bins).paginate(page=page, per_page=5)
#     waste = len(caneca.items)
#     # post = Post.query.filter_by(bins=bins).first_or_404()
#     # posts = Post.query.filter_by(bins=bins)\
#     # .order_by(Post.date_posted.desc())\
#     # .paginate(page=page, per_page=5)
#     return render_template('bins.html', form=form ,title=bins, caneca=caneca, waste = waste)

# @posts.route('/post/bins')
# def basura(bins):
#     # bins = Post.query.get_or_404(bins)
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter_by(bins='Green Bin').paginate(page=page, per_page=5)
#     form = FindForm()
#     return render_template('bins.html', title='Bins', posts=posts, form=form)

# @posts.route('/post/bins/1')
# def basura():
#     # bins = Post.query.get_or_404(bins)
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.filter_by(bins='Green Bin').paginate(page=page, per_page=5)
#     form = FindForm()
#     return render_template('bins.html', title='Bins', posts=posts, form=form)

# @posts.route('/post/bins/<int:bins>')
# def basura(bins):
#     page = request.args.get('page', 1, type=int)
#     posts = Post.query.get_or_404(bins).paginate(page=page, per_page=5)
#     form = FindForm()
#     return render_template('bins.html', posts=posts, form=form)


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