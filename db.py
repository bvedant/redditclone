import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('reddit_clone.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

def create_user(username, password):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def create_post(title, content, user_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, user_id, created_at) VALUES (?, ?, ?, ?)',
                 (title, content, user_id, datetime.now()))
    conn.commit()
    conn.close()

def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC').fetchall()
    conn.close()
    return posts

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT posts.*, users.username FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = ?', (post_id,)).fetchone()
    conn.close()
    return post

def update_votes(post_id, value):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET votes = votes + ? WHERE id = ?', (value, post_id))
    conn.commit()
    conn.close()

def create_comment(content, user_id, post_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (content, user_id, post_id, created_at) VALUES (?, ?, ?, ?)',
                 (content, user_id, post_id, datetime.now()))
    conn.commit()
    conn.close()

def get_comments(post_id):
    conn = get_db_connection()
    comments = conn.execute('SELECT comments.*, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = ? ORDER BY comments.created_at', (post_id,)).fetchall()
    conn.close()
    return comments