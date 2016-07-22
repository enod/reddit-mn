# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'temporary key'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/posts"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# create db
db = SQLAlchemy(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash(u'Нэвтрэн орно уу?')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def home():
    return render_template('public_home.html')


@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "admin" or request.form["password"] != "admin":
            error = u'Алдаа гарлаа. Шалгаад дахин нэвтэрнэ үү?'
        else:
            session['logged_in'] = True
            flash(u'Амжилттай нэвтэрлээ!')
            return redirect(url_for('user_home'))
    return render_template("login.html", error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
