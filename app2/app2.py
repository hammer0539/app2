from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from PIL import Image
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'umasecretkeymuitosegura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Bem-vindo à Aplicação Web Flask!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/fetch-image')
def fetch_image():
    url = 'https://exemplo.com/imagem.jpg'
    response = requests.get(url, stream=True)
    img = Image.open(response.raw)
    img.save('imagem_salva.jpg')
    return "Imagem salva com sucesso!"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
