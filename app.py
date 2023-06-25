import csv
from io import BytesIO, TextIOWrapper
from flask import Flask, current_app, render_template, request, redirect, send_file, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import cv2
import os
import tempfile
from flask_marshmallow import Marshmallow


app = Flask(__name__, static_folder='static', template_folder='templates')

marsh = Marshmallow(app)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certgen.sqlite3' 
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

        if username == 'mic' and password == '1234':
            flash("Certificate Generator says: Successfully logged in!", 'success')
            return redirect(url_for('admin'))
        else:
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



import datetime

@app.route('/generator', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        event_name = request.form.get('event')
        participant_name = request.form.get('name')
        award_name = request.form.get('award')

        if participant_name:
            # Load the certificate template
            certificate_template_path = os.path.join(app.root_path, 'certificatetemplate.png')
            certificate_template = cv2.imread(certificate_template_path)

            # Function to place the name, event name, and award name on the certificate at appropriate locations
            def place_text_on_certificate(certificate, text, position):
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 2.5
                font_color = (0, 0, 0)  # Black
                thickness = 2

                text_size = cv2.getTextSize(text, font, font_scale, thickness)
                text_x = int(position[0] - text_size[0][0] / 2)  # Center the text horizontally
                text_y = int(position[1] + text_size[0][1] / 2)  # Center the text vertically

                cv2.putText(certificate, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

            # Generate the certificate
            certificate = certificate_template.copy()

            # Place the participant name, event name, and award name on the certificate
            place_text_on_certificate(certificate, participant_name, (certificate.shape[1] // 2, 650))
            place_text_on_certificate(certificate, event_name, (certificate.shape[1] // 2, 1025))
            place_text_on_certificate(certificate, award_name, (certificate.shape[1] // 2, 890))

            # Create a temporary file to store the certificate image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_file_path = temp_file.name
                current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{participant_name}_{current_datetime}_certificate.png"
                cv2.imwrite(temp_file_path, certificate)

            # Prepare the file to be downloaded by the user
            response = current_app.make_response(send_file(temp_file_path, mimetype='image/png'))
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return response

        else:
            return "Please enter participant name."

    return render_template("generator.html", event="", name="", award="")





    
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
