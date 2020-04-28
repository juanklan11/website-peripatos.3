from flask import render_template, request, Blueprint, url_for, flash, redirect
from loginpage.models import Post
from loginpage.posts.forms import FindForm
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():

    suffix = '.png'
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
            return render_template('results.html', post=post, form=form, amount=amount)
    return render_template('home.html', posts=posts, form=form, title='Home', suffix=suffix)

@main.route("/about")
def about():
    return render_template('about.html', title='About')



