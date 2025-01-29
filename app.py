import json

from flask import Flask, render_template, request, redirect, url_for

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
        new_post = {
            "id": len(posts) + 1,
            "author": request.form['author'],
            "title": request.form['title'],
            "content": request.form['content']
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            break

    save_posts(posts)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
