import json

from flask import Flask, render_template, request, redirect, url_for
from jinja2.lexer import newline_re

app = Flask(__name__)

def load_posts():
    try:
        with open("data.json", "r") as file:
            blog_posts = json.load(file)
            return blog_posts
    except:
        return FileNotFoundError

def save_posts(posts):
    with open("data.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def home():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        posts = load_posts()
        new_id = max((post["id"] for post in posts), default=0) + 1  # Ensure a unique ID
        new_post = {
            "id": new_id,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['content']
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            break

    save_posts(posts)
    return redirect(url_for("home"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Load posts
    posts = load_posts()
    post = None
    for p in posts:
        if p["id"] == post_id:
            post = p
            break
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        # Update existing post
        post["author"] = request.form['author']
        post["title"] = request.form['title']
        post["content"] = request.form['content']

        save_posts(posts)
        return redirect(url_for('home'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    # Load posts
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:

            post["likes"] = post.get("likes", 0) + 1
            save_posts(posts)
            return redirect(url_for("home"))

    # If the post is not found, return a 404 error
    return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True)
