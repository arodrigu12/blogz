from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from helpers import is_valid

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'y337kGcys&zP3B'

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
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

    def __init__(self, username, password):

        self.username = username
        self.password = password

#Gives as a chance to filter all incoming requests
@app.before_request
def require_login():
    #Pages user can see without loging in
    allowed_routes = ['login', 'signup', 'blog', 'index']

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])

def login():

    username=''
    password=''
    username_error=''
    pwd_error=''

    if request.method == 'POST':
        username= request.form['username'].strip()
        password = request.form['password'].strip()
        user = User.query.filter_by(username=username).first()

        if not user:
            username_error = 'User name does not exist'

        elif user.password != password:
            pwd_error = 'Password is incorrect'
            password = ''

        else:
            #remember that user has logged in
            session['username'] = username          
            return redirect('/newpost')

    return render_template('login.html',
        title='Blogz',
        username=username,
        password=password,
        username_error=username_error,
        pwd_error=pwd_error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    username = ''
    password = ''
    username_error=''
    pwd_error=''
    verify_pwd_error=''
    error_condition=False

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        verify_pwd = request.form['verify']

        if not username:
            username_error="You must provide a username"
            error_condition=True
        elif not is_valid(username):
            username_error="Provide valid username of 3-20 characters (numbers and letters only)"
            error_condition=True
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                username_error = 'Username already exists'
                error_condition=True

        if not password:
            pwd_error="You must provide a password"
            error_condition=True
        elif not is_valid(password):
            pwd_error="You must provide a valid password of 3-20 characters (numbers and letters only)"
            error_condition=True
        elif password != verify_pwd:
            verify_pwd_error="Passwords do not match"
            error_condition=True

        if not error_condition:
            new_user = User(username, password)      
            db.session.add(new_user)
            db.session.commit()
            #"remember" the user
            session['username'] = username
            return redirect('/newpost')
        else:
            #Always clear password fields under any error conditions, for security.
            password=''

    return render_template('signup.html',
        title='Blogz',
        username=username,
        password=password,
        username_error=username_error,
        pwd_error=pwd_error,
        verify_pwd_error=verify_pwd_error)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

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
            owner = User.query.filter_by(username=session['username']).first()
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect("/blog?id=" + str(new_blog.id))

    return render_template('newpost.html', title="Blogz",
        no_title_error=no_title_error, no_body_error=no_body_error, body=body, blog_title=title)

@app.route('/blog')
def blog():

    blog_id = request.args.get('id')
    blogger_id = request.args.get('user')

    if not blog_id and not blogger_id:
        blog_entries = Blog.query.all()

        return render_template('blog.html', title="Blogz", 
            blog_entries=blog_entries)

    elif blog_id: #Show blog individually

        blog_obj = Blog.query.filter_by(id=blog_id).first()
        return render_template('display_blog.html', title="Blogz", 
            blog_obj=blog_obj)

    else: #Show a single blogger's posts

        blogger_posts = Blog.query.filter_by(owner_id=blogger_id).all()
        return render_template('display_blogger_posts.html',
            title="Blogz", blogger_posts=blogger_posts)

@app.route('/')
def index():

    bloggers = User.query.all()
    return render_template('index.html', title='Blogz', bloggers=bloggers)



if __name__ == '__main__':
    app.run()