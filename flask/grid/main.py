from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, current_user
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import subprocess
import config


# Инициализация приложения и бд
app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:12345678@localhost/grid_and_cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)


# models:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Integer, default=0)


class Namespaces(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)


class UserNamespaces(db.Model, UserMixin):
    name = db.Column(db.String(40), db.ForeignKey('namespaces.name'), primary_key=True)
    login = db.Column(db.String(128), db.ForeignKey('user.login'), primary_key=True)
    full_right = db.Column(db.Integer, default=0)


class Sshkeys(db.Model, UserMixin):
    login = db.Column(db.String(128), db.ForeignKey('user.login'))
    key = db.Column(db.String(700), nullable=False)
    name = db.Column(db.String(40), primary_key=True)


db.create_all()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#login, create root and admin:
# @app.route('/', methods=['GET'])
# def hello_world():
#     return render_template('index.html')


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return render_template('admin.html', content=user.login)
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


@app.route('/admin/manageusers/createusers', methods=['GET', 'POST'])
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
                if User.query.filter_by(login=login).first():
                    flash('user is already exist')
                else:
                    hash_pwd = generate_password_hash(password)
                    new_user = User(login=login, password=hash_pwd, is_admin=0)
                    db.session.add(new_user)
                    db.session.commit()
                    file='createUser.sh'
                    subproc = subprocess.Popen([config.path+file, login], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    subproc.wait()
                    return redirect(url_for('manage_users'))
    else:
        return redirect(url_for('user'))

    return render_template('createusers.html')


@app.route('/admin/manageusers/showusers', methods=['GET', 'POST'])
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
        conn = UserNamespaces.query.filter_by(login=login).all()
        if not user:
            flash('This user not exist')
        else:
            db.session.delete(user_d)
            for c in conn:
                db.session.delete(c)
            db.session.commit()
            return redirect(url_for('show_users'))

    return render_template('showusers.html', content=users)


@app.route('/admin/managenamespaces', methods=['GET', 'POST'])
@login_required
def manage_namespaces():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return render_template('managenamespaces.html')
    else:
        return redirect(url_for('user'))


@app.route('/admin/managenamaespaces/createnamespaces', methods=['GET', 'POST'])
@login_required
def create_namespaces():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        name = request.form.get('namespaces')

        if request.method == 'POST':
            if not (name):
                flash('Please, fill all fields!')
            else:
                if Namespaces.query.filter_by(name=name).first():
                    flash('namespace already exist')
                else:
                    new_namespaces = Namespaces(name=name)
                    db.session.add(new_namespaces)
                    db.session.commit()
                    return redirect(url_for('manage_namespaces'))
    else:
        return redirect(url_for('user'))

    return render_template('createnamespaces.html')


@app.route('/admin/manageusers/shownamespaces', methods=['GET', 'POST'])
@login_required
def show_namespaces():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 0:
        return redirect(url_for('user'))
    users = []
    namespaces = []
    for u in User.query.filter_by(is_admin=0):
        users.append(str(u.login))
    for n in Namespaces.query.order_by(Namespaces.id).all():
        namespaces.append(str(n.name))
    if request.method == 'POST':
        user_ = request.form.get('user')
        namespace_ = request.form.get('namespaces')
        full = request.form.get('rights')
        if full == 'full':
            full = 1
        else:
            full = 0
        un = UserNamespaces.query.filter_by(name=namespace_, login=user_).first()
        if un:
            flash('This connect already exist')
        else:
            new_el = UserNamespaces(name=namespace_, login=user_, full_right=full)
            db.session.add(new_el)
            db.session.commit()
            return redirect(url_for('show_namespaces'))

    return render_template('shownamespaces.html', users=users, namespaces=namespaces)


@app.route('/admin/manageusers/showconnects', methods=['GET', 'POST'])
@login_required
def show_connects():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 0:
        return redirect(url_for('user'))
    users = []
    for u in UserNamespaces.query.order_by(UserNamespaces.login):
        if u.full_right==1:
            f = 'full'
        else:
            f = 'not full'
        users.append((str(u.login), str(u.name), f))
    if request.method == 'POST':
        u = request.form.get('right')
        u = u.split()
        if u[2] == 'full':
            f = 0
        else:
            f = 1
        un = UserNamespaces.query.filter_by(name=u[0], login=u[1]).first()
        db.session.delete(un)
        new_c = UserNamespaces(name=u[0], login=u[1], full_right=f)
        db.session.add(new_c)
        db.session.commit()

        return redirect(url_for('show_connects'))

    return render_template('showconnects.html', content=users, content1=users)


#here
@app.route('/admin/manageusers/deleteconnections', methods=['GET', 'POST'])
@login_required
def delete_connections():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 0:
        return redirect(url_for('user'))
    users = []
    for u in UserNamespaces.query.order_by(UserNamespaces.login):
        users.append((str(u.login), str(u.name)))
    if request.method == 'POST':
        conn = request.form.get('connect')
        conn = conn.split()
        c = UserNamespaces.query.filter_by(name=conn[1], login=conn[0]).first()
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('delete_connections'))

    return render_template('deleteconnections.html', content=users)


@app.route('/', methods=['GET', 'POST'])
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
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response

#user:
@app.route('/user', methods=['GET'])
@login_required
def user():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 0:
        return render_template('user.html', conent=user.login)
    else:
        return redirect(url_for('admin'))


@app.route('/user/managessh', methods=['GET'])
@login_required
def manage_ssh():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    return render_template('managessh.html')


@app.route('/user/manageclusters', methods=['GET', 'POST'])
@login_required
def manage_clusters():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    # if check.full_right == 0:
    #     flash("No access")
    #     return redirect(url_for('user'))
    return render_template('manageclusters.html')


@app.route('/user/managessh/showssh', methods=['GET', 'POST'])
@login_required
def show_ssh():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    keys = []
    for k in Sshkeys.query.filter_by(login=user.login):
        keys.append((str(k.name), str(k.key)))
        #keys.append(str(k.name))
    if request.method == 'POST':
        name = request.form.get('name')
        ssh_name = Sshkeys.query.filter_by(name=name).first()
        if not ssh_name:
            flash('This ssh not exist')
        else:
            db.session.delete(ssh_name)
            db.session.commit()
            nfile = 'delSSH4user.sh'
            subproc = subprocess.Popen([config.path+nfile, user.login, ssh_name.key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subproc.wait()
            return redirect(url_for('show_ssh'))
    return render_template('showssh.html', content=keys)


@app.route('/admin/managessh/createssh', methods=['GET', 'POST'])
@login_required
def create_ssh():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    name = request.form.get('name')
    ssh = request.form.get('ssh')

    if request.method == 'POST':
        if not (name or ssh):
            flash('Please, fill all fields!')
        else:
            if Sshkeys.query.filter_by(name=name).first():
                flash('user is already exist')
            else:
                new_ssh = Sshkeys(login=user.login, name=name, key=ssh)
                db.session.add(new_ssh)
                db.session.commit()
                fname = 'addSSH4user.sh'
                subproc = subprocess.Popen([config.path+fname, user.login, ssh], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subproc.wait()
                return redirect(url_for('manage_ssh'))

    return render_template('createssh.html')


#manage clusters
@app.route('/user/choosenamespace', methods=['GET', 'POST'])
@login_required
def choose_namespace():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    namespaces = []
    for u in UserNamespaces.query.filter_by(login=user.login):
        namespaces.append(str(u.name))
    if request.method == 'POST':
        n = request.form.get('namespace')
        if not n:
            n = ''
        res = make_response(render_template('manageclusters.html'))
        res.set_cookie('namespace', n, max_age=60*60*24)
        return res
    return render_template('choosenamespace.html', content=namespaces)


@app.route('/admin/manageclusters/info', methods=['GET', 'POST'])
@login_required
def get_info():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'getClusterInfo.sh'
    namespace = request.cookies.get('namespace')
    subproc = subprocess.Popen([config.path+file, namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subproc.wait()
    # if subproc.stderr:
    #     flash('No clusters')
    #     output = subproc.stderr
    # else:
    #     output = subproc.stdout
    output = subproc.stdout
    output1 = subproc.stderr
    return render_template('stopcluster.html', content=output, content1=output1)


@app.route('/admin/manageclusters/stop', methods=['GET', 'POST'])
@login_required
def stop_cluster():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    # if not UserNamespaces.query.filter_by(login=user.login).first():
    #     flash("You haven't right")
    # else:
    file = 'stopCluster.sh'
    namespace = request.cookies.get('namespace')
    subproc = subprocess.Popen([config.path + file, namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subproc.wait()
    # if subproc.stderr:
    #     flash(f'No active cluster in this namespace: {namespace}')
    #     output = subproc.stderr
    # else:
    #     output = subproc.stdout
    output = subproc.stdout
    output1 = subproc.stderr
    return render_template('stopcluster.html', content=output, content1=output1)


@app.route('/admin/manageclusters/start', methods=['GET', 'POST'])
@login_required
def start_cluster():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'startCluster.sh'
    namespace = request.cookies.get('namespace')
    subproc = subprocess.Popen([config.path+file, namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subproc.wait()
    # if subproc.stderr:
    #     flash('No clusters')
    #     output = subproc.stderr
    # else:
    #     output = subproc.stdout
    output = subproc.stdout
    output1 = subproc.stderr
    return render_template('stopcluster.html', content=output, content1=output1)


@app.route('/admin/manageclusters/delete', methods=['GET', 'POST'])
@login_required
def delete_cluster():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'deleteCluster.sh'
    namespace = request.cookies.get('namespace')
    r = UserNamespaces.query.filter_by(login=user.login, name=namespace).first()
    if r.full_right == 0:
        flash('No rights')
    else:
        subproc = subprocess.Popen([config.path+file, namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        # if subproc.stderr:
        #     flash('No clusters')
        #     output = subproc.stderr
        # else:
        #     output = subproc.stdout
        output = subproc.stdout
        output1 = subproc.stderr
        return render_template('stopcluster.html', content=output, content1=output1)
    return render_template('stopcluster.html')


@app.route('/user/manageclusters/addssh', methods=['GET', 'POST'])
@login_required
def add_ssh():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'addSSHkey.sh'
    namespace = request.cookies.get('namespace')
    keys = []
    for k in Sshkeys.query.filter_by(login=user.login):
        keys.append(k.name)
    if request.method == 'POST':
        k = request.form.get('key')
        ssh_name = Sshkeys.query.filter_by(name=k).first()
        subproc = subprocess.Popen([config.path+file, namespace, ssh_name.key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        output = subproc.stdout
        output1 = subproc.stderr
        return render_template('stopcluster.html', content=output, content1=output1)
    return render_template('addssh.html', content3=keys)


@app.route('/admin/manageclusters/delssh', methods=['GET', 'POST'])
@login_required
def del_ssh():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'delSSHkey.sh'
    namespace = request.cookies.get('namespace')
    keys = []
    for k in Sshkeys.query.filter_by(login=user.login):
        keys.append(k.name)
    if request.method == 'POST':
        k = request.form.get('key')
        ssh_name = Sshkeys.query.filter_by(name=k).first()
        subproc = subprocess.Popen([config.path+file, namespace, ssh_name.key], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        output = subproc.stdout
        output1 = subproc.stderr
        return render_template('stopcluster.html', content=output, content1=output1)
    return render_template('delssh.html', content3=keys)

@app.route('/admin/manageclusters/create', methods=['GET', 'POST'])
@login_required
def create_cluster():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))
    file = 'createCluster.sh'
    namespace = request.cookies.get('namespace')
    r = UserNamespaces.query.filter_by(login=user.login, name=namespace).first()
    if r.full_right == 0:
        flash('No rights')
    else:
        namespace = request.cookies.get('namespace')
        subproc = subprocess.Popen([config.path+file, namespace], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        output = subproc.stdout
        output1 = subproc.stderr
        return render_template('stopcluster.html', content=output, content1=output1)
    return render_template('stopcluster.html')

@app.route('/admin/manageclusters/manage', methods=['GET', 'POST'])
@login_required
def manage():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    if user.is_admin == 1:
        return redirect(url_for('admin'))

    file = 'createClusterConfig.py'
    namespace = request.cookies.get('namespace')
    r = UserNamespaces.query.filter_by(login=user.login, name=namespace).first()
    if r.full_right == 0:
        flash('No rights')
        f = ''
    else:
        f = '1'
        nodecount = request.form.get('nodecount')
        nodename = request.form.get('nodename')
        nodeimage = request.form.get('nodeimage')
        hostport = request.form.get('hostport')
        cpulimit = request.form.get('cpulimit')
        memorylimit = request.form.get('memorylimit')
        disklimit = request.form.get('disklimit')
        kernelimage = request.form.get('kernelimage')
        if request.method == 'POST':
            if not (nodecount and nodename and nodeimage and hostport and cpulimit and memorylimit and disklimit and kernelimage):
                flash('Please, fill all fields!')
            else:
                subproc = subprocess.Popen([config.path + file, namespace, nodecount, nodename, nodeimage, hostport, cpulimit, memorylimit, disklimit, kernelimage], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subproc.wait()
                output = subproc.stdout
                output1 = subproc.stderr
                return render_template('stopcluster.html', content=output, content1=output1, out=f)
    return render_template('manage.html', out=f)