from flask import Flask, render_template, redirect, url_for, flash, request, abort
from app import app


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')


@app.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')



@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect(url_for('login'))
