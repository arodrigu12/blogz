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

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    no_title_error = ''
    no_body_error = ''
    error_condition = False
    title = ''
    body = ''

    if request.method == 'POST': # POST for processing, GET for rendering
        title = request.form['title'].strip()
        body = request.form['body'].strip()

        if not title:
            no_title_error = 'Please enter a blog title'
            error_condition = True

        if not body:
            no_body_error = 'Please fill in the blog body'
            error_condition = True

        if not error_condition:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')

    return render_template('newpost.html', title="Build-a-Blog",
        no_title_error=no_title_error, no_body_error=no_body_error, body=body, blog_title=title)

@app.route('/blog')
def blog():
    blog_entries = Blog.query.all()

    return render_template('blog.html', title="Build-a-Blog", 
        blog_entries=blog_entries)


if __name__ == '__main__':
    app.run()