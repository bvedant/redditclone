from flask import Flask, render_template, session
import db
from auth import auth
from posts import posts
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(auth)
app.register_blueprint(posts)

@app.route('/')
def index():
    all_posts = db.get_posts()
    return render_template('index.html', posts=all_posts)

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)