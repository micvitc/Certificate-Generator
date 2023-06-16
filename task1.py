from flask import Flask, render_template

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/')
def home():
    return render_template("Website Final.html")

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/home')
def returnhome():
    return render_template("Website Final.html")


if __name__ == '__main__':
    app.run(debug=True)
