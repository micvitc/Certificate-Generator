from flask import Blueprint, render_template,request, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import User, Event



app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required

def profile():
    return render_template('landing.html', name=current_user.username)

@app.route('/dashboard/')
def dash():
    return render_template('dashboard.html')

@app.route('/create_event', methods=['POST'])
@login_required

def create_event():
    event_name = request.form.get('event_name')
    brandings = request.form.get('brandings')
    authorized_signatory = "Sample"
    participants = "Sample participant"
    winners = "Sample winner"

    event = Event(event_name=event_name, brandings=brandings, authorized_signatory=authorized_signatory,participants=participants,winners=winners)
    db.session.add(event)
    db.session.commit()
    # password = request.form.get('password')
    return redirect(url_for('app.index'))






















# from flask import Flask, render_template,redirect,request, url_for, Blueprint
# from flask_sqlalchemy import SQLAlchemy
# import random
# import string
# import uuid
# app = Blueprint('app', __name__)


# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Set the database URI
# # db = SQLAlchemy(app)

# # Define your User model
# # class User(db.Model):
# #     username = db.Column(db.String(80), nullable=False)
# #     email = db.Column(db.String(50), unique=True,nullable=False)
# #     register_number = db.Column(db.String(50),primary_key=True)
# #     password = db.Column(db.String(80), nullable=False)

# #     def _init_(self, username, email, register_number, password):
# #         self.username = username
# #         self.email = email
# #         self.register_number = register_number
# #         self.password = password


# # #Define your Event Model
# # class Event(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     event_name = db.Column(db.String(50))
# #     brandings = db.Column(db.String(50))
# #     authorized_signatory = db.Column(db.String(50))
# #     participants = db.Column(db.String(200))
# #     winners = db.Column(db.String(200))

# #     def _init_(self, event_name, brandings, authorized_signatory, participants, winners):
# #         self.event_name = event_name
# #         self.brandings = brandings
# #         self.authorized_signatory = authorized_signatory
# #         self.participants = participants
# #         self.winners = winners

# @app.route('/')
# def home():
#     # user = User.query.all()
#     # print(user[0].password)
#     return render_template('index.html')

# # @app.route('/login/', methods=['GET', 'POST'])
# # def login_page():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']

# #         user = User.query.filter_by(email=email, password=password).first()
# #         print(user,"Succceeded")
# #         if user:
# #             return redirect(url_for('landing', user=user, auth=True))
# #             # return render_template('landing.html', user = user, auth = True)
# #         else:
# #             return render_template('login.html')

# #     return render_template('login.html')

# # @app.route('/signup/', methods=('GET', 'POST'))
# # def signup():
# #     if request.method == 'POST':
# #         name = request.form['name']
# #         email = request.form['email']
# #         register_number = request.form['register-number']
# #         password = request.form['password']
# #         print(name,email,register_number,password)
# #         user = User(username=name, email=email, register_number=register_number, password=password)
# #         print(user)
# #         db.session.add(user)
# #         db.session.commit()

# #         return redirect('/login/')

# #     return render_template('signup.html')

# @app.route('/landing/')
# def landing():
#     return render_template('landing.html')

# @app.route('/dashboard/', methods=['GET', 'POST'])
# def dashboard():
#     if request.method == 'POST':
#         event_name = request.form['event_name']
#         brandings = request.form['brandings']
#         authorized_signatory = request.files['authorized_signatory']
#         participants = request.form.getlist('participants')
#         winners = request.form.getlist('winners')

#         if authorized_signatory:
#             filename = authorized_signatory.filename
#             authorized_signatory.save('uploads/' + filename)
#         else:
#             filename = ''

#         # event = Event(event_name, brandings, filename, ', '.join(participants), ', '.join(winners))
#         # db.session.add(event)
#         # db.session.commit()

#         return redirect('/landing/')

#     return render_template('dashboard.html')


# # from flask import Flask,render_template

# # app = Flask(_name_)

# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # @app.route('/login/')
# # def login_page():
# #     return render_template('login.html')

# # @app.route('/signup/')
# # def signup():
# #     return render_template('signup.html')

# # @app.route('/landing/')
# # def landing():
# #     return render_template('landing.html')

# # @app.route('/dashboard/')
# # def dashboard():
# #     return render_template('dashboard.html')

# # if _name_ == "_main_":
# #     app.run(debug=True )   

# # from flask import Flask, render_template, request, redirect
# # from flask_sqlalchemy import SQLAlchemy

# # app = Flask(_name_)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# # db = SQLAlchemy(app)

# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(50))
# #     email = db.Column(db.String(50), unique=True)
# #     register_number = db.Column(db.String(50))
# #     password = db.Column(db.String(50))

# #     def _init_(self, name, email, register_number, password):
# #         self.name = name
# #         self.email = email
# #         self.register_number = register_number
# #         self.password = password

# # class Event(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     event_name = db.Column(db.String(50))
# #     brandings = db.Column(db.String(50))
# #     authorized_signatory = db.Column(db.String(50))
# #     participants = db.Column(db.String(200))
# #     winners = db.Column(db.String(200))

# #     def _init_(self, event_name, brandings, authorized_signatory, participants, winners):
# #         self.event_name = event_name
# #         self.brandings = brandings
# #         self.authorized_signatory = authorized_signatory
# #         self.participants = participants
# #         self.winners = winners

# # @app.route('/')
# # def home():
# #     return render_template('index.html')



# # @app.route('/login/', methods=['GET', 'POST'])
# # def login_page():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']

# #         user = User.query.filter_by(email=email, password=password).first()

# #         if user:
# #             return redirect('/landing/')
# #         else:
# #             return render_template('login.html')

# #     return render_template('login.html')

# # @app.route('/signup/', methods=['GET', 'POST'])
# # def signup():
# #     if request.method == 'POST':
# #         name = request.form['name']
# #         email = request.form['email']
# #         register_number = request.form['register-number']
# #         password = request.form['password']

# #         user = User(name, email, register_number, password)
# #         db.session.add(user)
# #         db.session.commit()

# #         return redirect('/landing/')

# #     return render_template('signup.html')

# # @app.route('/landing/')
# # def landing():
# #     return render_template('landing.html')

# # @app.route('/dashboard/', methods=['GET', 'POST'])
# # def dashboard():
# #     if request.method == 'POST':
# #         event_name = request.form['event_name']
# #         brandings = request.form['brandings']
# #         authorized_signatory = request.files['authorized_signatory']
# #         participants = request.form.getlist('participants')
# #         winners = request.form.getlist('winners')

# #         if authorized_signatory:
# #             filename = authorized_signatory.filename
# #             authorized_signatory.save('uploads/' + filename)
# #         else:
# #             filename = ''

# #         event = Event(event_name, brandings, filename, ', '.join(participants), ', '.join(winners))
# #         db.session.add(event)
# #         db.session.commit()

# #         return redirect('/landing/')

# #     return render_template('dashboard.html')

# # if _name_ == "_main_":
# #     with app.app_context():
# #         db.create_all()
# #     app.run(debug=True)