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
    return render_template("tabulka.html")

@app.route('/dotaznik/<account_id>', methods=['GET'])
def zobraz_dotaznik(account_id):
    return render_template("dotaznik.html", account_id=account_id)

@app.route('/dotaznik/<account_id>', methods=['GET'])
def dotaznik_get(family_id):
    if request.method == 'GET':
        family_id = request.form["family_id"]

@app.route('/dotaznik/<account_id>', methods=['POST'])
def dotaznik_post (account_id):
    if request.method == 'POST':
        # vyplni tabulku family
        file_number = request.form["file_number"]
        approval_type_id = request.form["approval_type_id"]
        regional_office_id = request.form["regional_office_id"]
        expectation_status_id = request.form["expectation_status_id"]
        region_id = request.form["region_id"]
        district_id = request.form["district_id"]
        carer_info_id = request.form["carer_info_id"]
        prepcourse = request.form["prepcourse"]
        account_id = request.form["account_id"]
        # vyplni tabulku family_parent pro prvního rodiče
        family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
        sex_id = request.form["parent1_sex_id"]
        year_of_birth = request.form["parent1_year_of_birth"]
        databaze.insert_parent(family_id, sex_id, year_of_birth)
        # vyplni tabulku family_parent pro druhého rodiče
        family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
        sex_id = request.form["parent2_sex_id"]
        year_of_birth = request.form["parent2_year_of_birth"]
        databaze.insert_parent(family_id, sex_id, year_of_birth)
        # vyplni tabulku child_in_care pro nejmladší dítě v péči
        family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
        sex_id = request.form["youngest_child_sex_id"]
        year_of_birth = request.form["youngest_child_year_of_birth"]
        relationship_id = request.form["relationship_id"]
        databaze.insert_child_in_care(family_id, sex_id, year_of_birth, relationship_id)
        # vyplni tabulku expectation
        family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
        sex_id = request.form["expectation_sex_id"]
        databaze.insert_expectation(family_id, sex_id)
        # vyplni tabulku expectation_sibling_info
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        sibling_info_id = request.form["sibling_info_id"]
        databaze.insert_expectation_sibling_info(expectation_id, sibling_info_id)
        # vyplni tabulku expectation_mental_handicap
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        mental_handicap_id = request.form["mental_handicap_id"]
        databaze.insert_expectation_mental_handicap(expectation_id, mental_handicap_id)
        # vyplni tabulku expectation_physical_handicap
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        physical_handicap_id = request.form["physical_handicap_id"]
        databaze.insert_expectation_physical_handicap(expectation_id, physical_handicap_id)
        # vyplni tabulku expectation_ethnicity
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        expectation_ethnicity_id = request.form["expectation_ethnicity_id"]
        databaze.insert_expectation_ethnicity(expectation_id, expectation_ethnicity)
        # vyplni tabulku expectation_legal_status
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        expectation_legal_status_id = request.form["expectation_legal_status_id"]
        databaze.insert_expectation_legal_status(expectation_id, expectation_legal_status)
                # vyplni tabulku expectation_age
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        expectation_age_id = request.form["expectation_age_id"]
        databaze.insert_expectation_age(expectation_id, expectation_age)
                # vyplni tabulku expectation_anamnesis
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        expectation_anamnesis_id = request.form["expectation_anamnesis_id"]
        databaze.insert_expectation_anamnesis(expectation_id, expectation_anamnesis)
        






    return render_template("success.html")


@app.route('/login')
def login ():
    return render_template("login.html",
    )

@app.route('/success')
def success ():
    return render_template("success.html",
    )


