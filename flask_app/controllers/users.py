from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
# from flask_app.models.product import Tree
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("index.html", user=User.get_by_id(data))


@app.route('/user/shop')
def shop():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("shop.html", user=User.get_by_id(data))


@app.route('/team')
def team():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("team.html", user=User.get_by_id(data))


@app.route('/tech')
def tech():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("tech.html", user=User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
