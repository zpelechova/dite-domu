import functools
from flask import Flask, render_template, request, flash
import main
import databaze
import mail
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
        id_uzivatele = databaze.registrace_nr(email, password)
        if id_uzivatele:
            mail.email_dotaznik(email, id_uzivatele)
        else: 
            flash ('Někde se stala chyba, zkuste to prosím znovu', "warning")
    return render_template("success.html")

@app.route('/tabulka')
def tabulka ():
    vyber_z_databaze = databaze.return_family()
    return render_template("tabulka.html")

@app.route('/dotaznik')
def zobraz_dotaznik ():
    return render_template("dotaznik.html",
    )

@app.route('/dotaznik2/<account_id>', methods=['GET'])
def zobraz_dotaznik2(account_id):
    return render_template("dotaznik2.html", account_id=account_id)

@app.route('/dotaznik2/<account_id>', methods=['GET'])
def dotaznik2_get(family_id):
    if request.method == 'GET':
        family_id = request.form["family_id"]

# @app.route('/dotaznik2/<account_id>', methods=['POST'])
# def dotaznik2_post (account_id):
#     if request.method == 'POST':
#         file_number = request.form["file_number"]
#         approval_type_id = request.form["approval_type_id"]
#         regional_office_id = request.form["regional_office_id"]
#         expectation_status_id = request.form["expectation_status_id"]
#         region_id = request.form["region_id"]
#         district_id = request.form["district_id"]
#         carer_info_id = request.form["carer_info_id"]
#         prepcourse = request.form["prepcourse"]
#         account_id = request.form["account_id"]
#         # ziskat promenne pro tabulku family a vlozit zaznam, funkce ti vrati zpatky family id
#         # family_id = vloz_zaznam_do_tabulkyFamily(jmeno, prijmeni)
#         family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
#         sex_id = request.form["sex_id"]
#         year_of_birth = request.form["year_of_birth"]
#         databaze.insert_parent(family_id, sex_id, year_of_birth)
#         family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
#         sex_id = request.form["sex_id"]
#         year_of_birth = request.form["year_of_birth"]
#         relationship_id = request.form["relationship_id"]
#         databaze.insert_child_in_care(family_id, sex_id, year_of_birth, relationship_id)
#     return render_template("success.html")


@app.route('/login')
def login ():
    return render_template("login.html",
    )

@app.route('/success')
def success ():
    return render_template("success.html",
    )


