import flask
from flask import render_template, Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GifComV1.db'
db = SQLAlchemy(app)

class Gifs1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    Gifs = db.Column(db.String(255), nullable=False)

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

@app.route('/sendgif', methods=['POST', 'GET'])
def sendgif():
    if request.method == 'POST':
        title = request.form['title']
        Gifs = request.form['Gifs']

        post = Gifs1(title=title, Gifs=Gifs)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка'

    else:
        return render_template('sendgif.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)