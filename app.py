import io
import os.path

import flask
from flask import render_template, Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from moviepy.editor import VideoFileClip
from typing_extensions import reveal_type
from flask import send_file
from PIL import Image

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GifComV1.db'
db = SQLAlchemy(app)

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
            clip.resize(width=480).write_gif(output_path, fps=10, logger=None)

        with open(output_path, "rb") as f:
            gif_bytes = f.read()

        return gif_bytes

    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)


#Щоб гіф відправляти
@app.route('/sendgif', methods=['POST', 'GET'])
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




