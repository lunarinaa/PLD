from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

blog_posts = [
    {"id": 1, "title": "Post 1", "content": "Hello"},
    {"id": 2, "title": "Post 2", "content": "Sup guys"},
    {"id": 3, "title": "Post 3", "content": "Pld is boring"}

]

def get_next_id():
    if blog_posts:
        return max(post['id'] for post in blog_posts) + 1
    else:
        return 1

@app.route('/')
def homepage():
    return render_template('homepage.html', posts=blog_posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        abort(404)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {"id": get_next_id(), "title": title, "content": content}
        blog_posts.append(new_post)
        return redirect(url_for('homepage'))
    return render_template('add_post.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if not post:
        abort(404)

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        return redirect(url_for('homepage'))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    global blog_posts
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)
