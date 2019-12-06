from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(100), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Blog id ' + str(self.id)

@app.route('/home')
def hello_world():
    return render_template('index.html')  

@app.route('/posts', methods=['GET', 'POST', 'PUT'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_name = request.form['name']
        post_age = request.form['age']
        new_post = BlogSpot(title=post_title, name=post_name, age=post_age)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    elif request.method == 'PUT':
        post_title = request.form['title']
        print("==================>"+post_title)
        all_posts = BlogSpot.query.filter_by(title=post_title).all()
        return render_template('posts.html', posts= all_posts)
    else :
        all_posts = BlogSpot.query.order_by(BlogSpot.date_posted).all()
        return render_template('posts.html', posts= all_posts)

@app.route('/searchPosts/<int:id>', methods=['GET', 'POST', 'PUT'])
def searchPosts(id):
    post =BlogSpot.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.name = request.form['name']
        post.age = request.form['age']
        db.session.commit()
        return redirect('/posts')
    else :
        return render_template('edit.html', post=post)
    
@app.route('/deletePosts/<int:id>')
def deleteposts(id):
    post =BlogSpot.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
    

@app.route('/home/<name>', methods=['GET'])
def hello_world1(name):
    return "Welcome to my page. %s" % name

if __name__ == '__main__' :
    app.run(host="localhost", port=8000, debug=True)
