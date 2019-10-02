from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
     
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #SQLAlchemy should populate blogs list below with items from Blog class
    #such that the owner property is equal to the specific user under consideration
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):

        self.email = email
        self.password = password

@app.route('/login', methods=['POST', 'GET'])

def login():

    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            #remember that user has logged in
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash("User password incorrect or user does not exist", 'error')


    return render_template('login.html')


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
            owner = User.query.filter_by(email=session['email']).first()
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect("/blog?id=" + str(new_blog.id))

    return render_template('newpost.html', title="Build-a-Blog",
        no_title_error=no_title_error, no_body_error=no_body_error, body=body, blog_title=title)

@app.route('/blog')
def blog():

    blog_id = request.args.get('id')

    if not blog_id:
        blog_entries = Blog.query.all()

        return render_template('blog.html', title="Build-a-Blog", 
            blog_entries=blog_entries)

    else:

        blog_obj = Blog.query.filter_by(id=blog_id).first()
        return render_template('display_blog.html', title="Build-a-Blog", 
            blog_obj=blog_obj)


if __name__ == '__main__':
    app.run()