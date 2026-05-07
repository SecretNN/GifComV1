import flask
from flask import render_template, Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GifComV1.db'
db = SQLAlchemy(app)

class Gifs1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    text = db.Column(db.Text, nullable=False)

@app.route('/main')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/mygif')
def mygif():
    return render_template('mygif.html')

@app.route('/sendgif')
def sendgif():
    return render_template('sendgif.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)