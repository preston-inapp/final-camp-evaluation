from distutils.errors import CompileError
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Comment, Post, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
def all_posts():
    posts = Post.query.all()
    users = User.query.all()
    return render_template('all_posts.html', posts=posts, user=current_user, users=users)


# View blog posts created by a user
@views.route('/myposts')
@login_required
def home():
    return render_template("view_posts.html", user=current_user)

# View an individual post
@views.route('/post/<postId>', methods=['GET', 'POST'])
def viewpost(postId):
    if request.method == 'POST':
        data = request.form.get('data')
        user_id = request.form.get('user_id')
        new_comment = Comment(data=data, user_id=user_id, post_id=postId)
        db.session.add(new_comment)
        db.session.commit()
        print('Post added successfully')
    post = Post.query.get(postId)
    author = User.query.get(post.user_id)
    users = User.query.all()  
    return render_template('view_a_post.html', post=post, user=current_user, author=author, users=users)

#Create a new post
@views.route('/new-post', methods=['GET', 'POST'])
@login_required
def newPost():
    if request.method == 'POST':
        post = request.form.get('post')
        title = request.form.get('title')


        if len(post) < 1:
            flash('Post is too short!', category='error')
        else:
            new_post = Post(data=post, user_id=current_user.id, title=title)
            db.session.add(new_post)
            db.session.commit()
            flash('Blog post added!', category='success')
        return redirect(url_for('views.home'))
    return render_template("create_post.html", user=current_user)



@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})
