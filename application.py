import os
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm, SearchForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'r\x86/\x1d\x92\xa7\x043\x02\x97\xc6\xee\xf8\xaf\x07\x97'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True)
    user_email = db.Column('user_email',db.String(50), unique=True)
    username = db.Column('username', db.String(50), unique=True)
    password = db.Column('password', db.String(50), unique=False)
    book = db.relationship('Books', backref='read', lazy=True)

    def __init__(self, user_email, username, password, confirm_password):
            self.user_email = user_email
            self.username = username
            self.password = generate_password_hash(password)


    def __repr__(self):
            return '<User %r>' % (self.username)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column('isbn', db.String(13), primary_key=True)
    title = db.Column('title', db.String(100), unique=False)
    author = db.Column('author', db.String(50), unique=False)
    year = db.Column('year', db.Integer,unique=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __init__(self,title, author, year):
            self.title = title
            self.author = author
            self.year = year

    def __repr__(self):
            return '<Books %r>' %(self.title)



#db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():

    image_books = url_for('static', filename="books.jpg")
    image_college = url_for('static', filename="college.jpg")

    return render_template("index.html", image_books=image_books , image_college=image_college)


@app.route("/register", methods=["GET"])
def show_register():
    return render_template("register.html", form=RegistrationForm())


@app.route("/register", methods=["POST"])
def register():

    form = RegistrationForm(request.form)
    hashed_password = generate_password_hash(form.password.data)
    user_email = request.form.get("user_email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = hashed_password
    user = User.query.filter_by(user_email=user_email).first()
    if not user_email or not username:
        flash(u'fields should not be empty', 'warning')
        return redirect(url_for('register'))

    if user:
        flash(u'Email address already exists.', 'warning')
        return redirect(url_for('register'))

    new_user = User(user_email=user_email, username=username, password=password, confirm_password=confirm_password)

    db.session.add(new_user)
    db.session.commit()
    flash(u'Your account has been created.You can now login.', 'success')
    return redirect(url_for('login'))


@app.route("/login", methods=["GET"])
def login():
        session['next'] = request.args.get('next')
        image_file = url_for('static', filename="css/college_library.jpg")
        return render_template("login.html", image_file=image_file)


@app.route('/login', methods=['POST'])
def login_post():
    user_email = request.form['user_email']
    password = request.form['password']

    user = User.query.filter_by(user_email=user_email).first()
    if not user_email or not check_password_hash(user.password, password):
            flash(u'Invalid credentials','warning')
            return redirect(url_for('login'))
    login_user(user, remember=False)
    flash(u'You were successfully logged in ','success')
    return redirect(url_for('afterlogin'))



@app.route("/after-login", methods=["POST", "GET"])
@login_required
def afterlogin():

    return render_template("after-login.html")



@app.route('/search_results', methods=['POST'])
@login_required
def search_result():
   title = request.form['title']

   titles= Books.query.filter(Books.title.like('%'+title+'%')).all()
   if not titles:
       flash('0 result found','warning')
       return redirect(url_for('afterlogin'))
   else:
       flash('Search result found', 'success')
   return render_template('search_result.html', titles=titles)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":

    db.create_all()
app.run(debug=True)