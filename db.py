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


def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY votes DESC').fetchall()
    conn.close()

    return posts


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    return post


def create_post(title, content, author):
    conn = get_db_connection()
    conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                 (title, content, author))
    conn.commit()
    conn.close()


def update_votes(post_id, value):
    conn = get_db_connection()
    conn.execute('UPDATE posts SET votes = votes + ? WHERE id = ?',
                 (value, post_id))
    conn.commit()
    conn.close()


def get_comments(post_id):
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments WHERE post_id = ? ORDER BY created_at', (post_id,)).fetchall()
    conn.close()
    
    return comments


def create_comment(content, author, post_id):
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (content, author, post_id) VALUES (?, ?, ?)',
                 (content, author, post_id))
    conn.commit()
    conn.close()
