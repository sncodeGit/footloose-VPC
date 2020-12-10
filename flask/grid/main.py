from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, current_user
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


# Инициализация приложения и бд
app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:12345678@localhost/grid_and_cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)


# models:
class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0)


# class Namespaces(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(40), unique=True)
#     login = db.Column(db.String(128), db.ForeignKey('user.login'))


db.create_all()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#routes:
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return render_template('admin.html')
    else:
        return redirect(url_for('user'))


@app.route('/admin/manageusers', methods=['GET'])
@login_required
def manage_users():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return render_template('manageusers.html')
    else:
        return redirect(url_for('user'))


@app.route('/admim/manageusers/createusers', methods=['GET', 'POST'])
@login_required
def create_users():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if request.method == 'POST':
            if not (login or password or password2):
                flash('Please, fill all fields!')
            elif password != password2:
                flash('Passwords are not equal!')
            else:
                hash_pwd = generate_password_hash(password)
                new_user = User(login=login, password=hash_pwd, is_admin=0)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('manage_users'))
    else:
        return redirect(url_for('user'))

    return render_template('createusers.html')


@app.route('/admim/manageusers/showusers', methods=['GET', 'POST'])
@login_required
def show_users():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 0:
        return redirect(url_for('user'))
    users = []
    for u in User.query.filter_by(is_admin=0):
        users.append(str(u.login))
    if request.method == 'POST':
        login = request.form.get('login')
        user_d = User.query.filter_by(login=login).first()
        if not user:
            flash('This user not exist')
        else:
            db.session.delete(user_d)
            db.session.commit()
            return redirect(url_for('show_users'))

    return render_template('showusers.html', content=users)


@app.route('/admim/managenamespaces', methods=['GET', 'POST'])
@login_required
def manage_namespaces():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return render_template('managenamespaces.html')
    else:
        return redirect(url_for('user'))


#here
@app.route('/admim/managenamaespaces/createnamespaces', methods=['GET', 'POST'])
@login_required
def create_namespaces():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if request.method == 'POST':
            if not (login or password or password2):
                flash('Please, fill all fields!')
            elif password != password2:
                flash('Passwords are not equal!')
            else:
                hash_pwd = generate_password_hash(password)
                new_user = User(login=login, password=hash_pwd, is_admin=0)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('manage_users'))
    else:
        return redirect(url_for('user'))

    return render_template('createusers.html')


@app.route('/user', methods=['GET'])
@login_required
def user():
    return render_template('user.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    ad = User.query.filter_by(is_admin=1).first()
    if not ad:
        return redirect(url_for('register'))
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # next_page = request.args.get('next')
            if user.is_admin == 1:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user'))
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, is_admin=1)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response