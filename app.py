import io
import os.path

import flask
from flask import render_template, Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from moviepy import VideoFileClip
from sqlalchemy.sql.functions import current_user
from typing_extensions import reveal_type
from flask import send_file
from PIL import Image
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GifComV1.db'
db = SQLAlchemy(app)
#Для Flask login
app.secret_key = 'super-secret-key-change-me'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
#бд для акків
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #чек бази
        user = User.query.filter_by(username=username).first()
        #правильно чи нє
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        return 'Щось не те ти ввів'
    return render_template('login.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('signup.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
#Видалити гіф (Дозволяю тільки  "Адміну"
@app.route('/delete/<int:id>')
@login_required
def delete_gif(id):
    #Замінити Secret На тої нік, який повинен бути адміном
    if current_user.username != 'Secret':
        return redirect(url_for('home'))
    gif_delete = Gifs1.query.get_or_404(id)
    try:
        db.session.delete(gif_delete)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "Десь помилка!1!"




#Тута PIL не хоче дружити з moveipy, це вже крайня міра
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
#Для  бази (данних)
class Gifs1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
#Щоб завжди база данних була
with app.app_context():
    db.create_all()

#меін сторінка
@app.route('/main')
@app.route('/')
def home():
    items = Gifs1.query.all()
    return render_template('home.html', items=items)
#профіль
@app.route('/profile')
def profile():
    items = Gifs1.query.all()
    return render_template('profile.html', items=items)

@app.route('/mygif')
def mygif():
    return render_template('mygif.html')


#щоб с відео робились гіфки, ігнорувалися фото та гіф (не треба для них конвертація)
def video2gif(file_storage):
    input_path = "temp_input__" + file_storage.filename
    output_path = "temp_output.gif"

    file_storage.save(input_path)

    filename = file_storage.filename.lower()

    try:
        if filename.endswith('.gif'):
            with open(input_path, "rb") as f:
                return f.read()

        if not filename.endswith(('.mp4', '.mov', '.avi')):
            with Image.open(input_path) as img:
                byte_io = io.BytesIO()
                img.save(byte_io, format='GIF')
                return byte_io.getvalue()

        with VideoFileClip(input_path) as clip:
            clip.resized(width=480).write_gif(output_path, fps=12, logger=None)

        with open(output_path, "rb") as f:
            gif_bytes = f.read()

        return gif_bytes

    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)


#Щоб гіф відправляти
@app.route('/sendgif', methods=['POST', 'GET'])
@login_required
def sendgif():
    if request.method == 'POST':
        title = request.form.get('title')
        file = request.files.get('gif_file')


        if file and title:
            binary_data =video2gif(file)

            new_gif = Gifs1(title=title, data=binary_data)
            db.session.add(new_gif)
            db.session.commit()
            return  redirect('/')
        return "Помилка, не вибрали файл або назву", 400

    else:
        return render_template('sendgif.html')



@app.route('/get_gif/<int:id>')
def get_gif(id):
    item = Gifs1.query.get(id)
    return send_file(io.BytesIO(item.data), mimetype='image/gif')


#ПУСК
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




