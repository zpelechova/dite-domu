import functools
from flask import Flask, render_template, request
import databaze
import gunicorn
app = Flask("MojeAppka")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index ():
    return render_template("index.html")

@app.route('/registrace_ku')
def zobraz_registraci_ku ():
    return render_template("registrace_ku.html")

@app.route('/registrace_ku', methods=('GET', 'POST'))
def registrace_ku():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position_name = request.form['position_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        databaze.registrace_ku(first_name, last_name, position_name, email, password, phone)
    return render_template('/success.html')

@app.route('/registrace_nr')
def zobraz_registraci_nr ():
    return render_template("registrace_nr.html")

@app.route('/registrace_nr', methods=('GET', 'POST'))
def registrace_nr ():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        databaze.registrace_nr(email, password)
    return render_template("success.html")

@app.route('/tabulka')
def tabulka ():
    return render_template("tabulka.html")

@app.route('/dotaznik')
def zobraz_dotaznik ():
    return render_template("dotaznik.html",
    )

@app.route('/dotaznik', methods=('GET', 'POST'))
def dotaznik ():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        databaze.registrace_nr(email, password)
    return render_template("success.html")

@app.route('/login')
def login ():
    return render_template("login.html",
    )

@app.route('/success')
def success ():
    return render_template("success.html",
    )
