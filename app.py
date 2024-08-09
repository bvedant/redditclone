from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import db

app = Flask(__name__)


@app.route('/')
def index():
    posts = db.get_posts()

    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = db.get_post(post_id)
    comments = db.get_comments(post_id)

    return render_template('post.html', post=post, comments=comments)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        db.create_post(title, content, author)

        return redirect(url_for('index'))
    
    return render_template('create.html')


@app.route('/vote/<int:post_id>/<int:value>')
def vote(post_id, value):
    db.update_votes(post_id, value)

    return redirect(url_for('index'))


@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    content = request.form['content']
    author = request.form['author']
    db.create_comment(content, author, post_id)

    return redirect(url_for('post', post_id=post_id))


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
