from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(250))
    
    def __init__(self, title, body):
     
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST': # POST for processing, GET for rendering
        title = request.form['title']
        body = request.form['body']   
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

    blog_entries = Blog.query.all()

    return render_template('index.html', title="Build-a-Blog", 
        blog_entries=blog_entries)

if __name__ == '__main__':
    app.run()