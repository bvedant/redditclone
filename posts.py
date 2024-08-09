from flask import Blueprint, request, session, redirect, url_for, flash, render_template
import db

posts = Blueprint('posts', __name__)

@posts.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        flash('You must be logged in to create a post.')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.create_post(title, content, session['user_id'])
        flash('Post created successfully.')
        return redirect(url_for('index'))
    return render_template('create.html')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = db.get_post(post_id)
    comments = db.get_comments(post_id)
    return render_template('post.html', post=post, comments=comments)

@posts.route('/vote/<int:post_id>/<int:value>')
def vote(post_id, value):
    if 'user_id' not in session:
        flash('You must be logged in to vote.')
        return redirect(url_for('auth.login'))
    db.update_votes(post_id, value)
    return redirect(url_for('index'))

@posts.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to comment.')
        return redirect(url_for('auth.login'))
    content = request.form['content']
    db.create_comment(content, session['user_id'], post_id)
    return redirect(url_for('posts.post', post_id=post_id))