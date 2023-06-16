import csv
from io import TextIOWrapper
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:gr8ani123@localhost:3306/certgen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))


class Admin(db.Model):
    __tablename__ = 'admin'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))


class Event(db.Model):
    __tablename__ = 'events'

    eventid = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('events.eventid'))
    participant_name = db.Column(db.String(50))
    award_name = db.Column(db.String(50))

    event = db.relationship('Event', backref=db.backref('participants', lazy=True))


@app.route('/')
def home():
    return render_template("Landing.html")


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Certificate Generator says: Please enter both username and password.", 'error')
            return redirect(url_for('home'))

        user = Admin.query.filter_by(username=username).first()

        if user and user.password == password:
            flash("Certificate Generator says: Successfully logged in!", 'success')
            return redirect(url_for('admin'))
        else:
            flash("Certificate Generator says: Invalid credentials", 'error')
            return redirect(url_for('adminlogin'))

    return render_template('Website Final1.html')


@app.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Certificate Generator says: Please enter both username and password.", 'error')
            return redirect(url_for(''))

        existing_user = Admin.query.filter_by(username=username).first()

        if existing_user:
            flash("Certificate Generator says: An account with this username already exists.", 'error')
            return redirect(url_for('adminlogin'))

        new_user = Admin(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Certificate Generator says: Successfully signed up!", 'success')
            return redirect(url_for('adminlogin'))
        except Exception as e:
            print(str(e))
            flash("Certificate Generator says: An error occurred while signing up.", 'error')
            return redirect(url_for('adminsignup'))

    return render_template('Login1.html')


@app.route('/usersignup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Certificate Generator says: Please enter both username and password.", 'error')
            return redirect(url_for(''))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Certificate Generator says: An account with this username already exists.", 'error')
            return redirect(url_for('home'))

        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Certificate Generator says: Successfully signed up!", 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(str(e))
            flash("Certificate Generator says: An error occurred while signing up.", 'error')
            return redirect(url_for('home'))

    return render_template('Login.html')


@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Certificate Generator says: Please enter both username and password.", 'error')
            return redirect(url_for('home'))

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            flash("Certificate Generator says: Successfully logged in!", 'success')
            return redirect(url_for('mainpage'))
        else:
            flash("Certificate Generator says: Invalid credentials", 'error')
            return redirect(url_for('userlogin'))

    return render_template('Website Final.html')


@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)


@app.route('/generator', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        event_name = request.form.get('event')
        participant_name = request.form.get('name')
        file = request.files.get('file')

        if event_name and participant_name:
            event = Event.query.filter_by(event_name=event_name).first()

            if not event:
                event = Event(event_name=event_name)
                db.session.add(event)
                db.session.commit()

            participant = Participant(eventid=event.eventid, participant_name=participant_name, award_name="")
            db.session.add(participant)
            db.session.commit()
            flash("Certificate Generator says: Details added successfully!", 'success')
        elif file:
            try:
                csv_data = TextIOWrapper(file, encoding='utf-8-sig')
                reader = csv.reader(csv_data)
                next(reader)  # Skip header row if present

                for row in reader:
                    event_name = row[0]
                    participant_name = row[1]

                    event = Event.query.filter_by(event_name=event_name).first()

                    if not event:
                        event = Event(event_name=event_name)
                        db.session.add(event)
                        db.session.commit()

                    participant = Participant(eventid=event.eventid, participant_name=participant_name,
                                              award_name="")
                    db.session.add(participant)

                db.session.commit()
                flash("Certificate Generator says: CSV data added successfully!", 'success')
            except Exception as e:
                flash("Certificate Generator says: An error occurred while processing the CSV file.", 'error')
                print(str(e))
        else:
            flash("Certificate Generator says: Please enter either event and participant name or upload a file.",
                  'error')

        return redirect(url_for('mainpage'))

    return render_template("generator.html")


@app.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Certificate Generator says: User deleted successfully!", 'success')
    else:
        flash("Certificate Generator says: User not found.", 'error')

    return redirect(url_for('admin'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
