import gviz_api
import json
import functools
from flask import Flask, render_template, request, flash
import databaze
import mail
import gunicorn
import logging
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
        district_id = request.form["district_id"]
        carer_info_id = request.form["carer_info_id"]
        prepcourse = request.form["prepcourse"]
        account_id = request.form["account_id"]
        note = request.form["note"]
        approval_date = request.form["approval_date"]
        number_child_in_care = request.form.get('number_child_in_care')
        family_id = databaze.insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care)
        # vyplni tabulku family_parent pro prvního rodiče
        parent1_sex_id = request.form["parent1_sex_id"]
        parent1_year_of_birth = request.form["parent1_year_of_birth"]
        databaze.insert_parent1(family_id, parent1_sex_id, parent1_year_of_birth)
        # vyplni tabulku family_parent pro druhého rodiče
        parent2_sex_id = request.form.get("parent2_sex_id")
        parent2_year_of_birth = request.form.get("parent2_year_of_birth")
        # if parent2_sex_id is not None and parent2_year_of_birth is not None:
        databaze.insert_parent1(family_id, parent2_sex_id, parent2_year_of_birth)
        # vyplni tabulku child_in_care pro nejmladší dítě v péči
        youngest_child_sex_id = request.form.get("youngest_child_sex_id")
        youngest_child_year_of_birth = request.form.get("youngest_child_year_of_birth")
        relationship_id = request.form.get("relationship_id")
        # if youngest_child_sex_id is not None and youngest_child_year_of_birth is not None and relationship_id is not None:
        databaze.insert_child_in_care(family_id, youngest_child_sex_id, youngest_child_year_of_birth, relationship_id)
        # vyplni tabulku expectation 
        sex_id = request.form["expectation_sex_id"]
        # vyplni tabulku expectation_sibling_info
        expectation_id = databaze.insert_expectation(family_id, sex_id)
        sibling_info_id = request.form.getlist("sibling_info_id")
        databaze.insert_expectation_sibling_info(expectation_id, sibling_info_id)
        # vyplni tabulku expectation_mental_handicap
        mental_handicap_id = request.form["mental_handicap_id"] 
        databaze.insert_expectation_mental_handicap(expectation_id, mental_handicap_id)
        # vyplni tabulku expectation_physical_handicap
        physical_handicap_id = request.form["physical_handicap_id"]
        databaze.insert_expectation_physical_handicap(expectation_id, physical_handicap_id)
        # vyplni tabulku expectation_ethnicity
        expectation_ethnicity_id = request.form.getlist("expectation_ethnicity_id")
        databaze.insert_expectation_ethnicity(expectation_id, expectation_ethnicity_id)
        # vyplni tabulku expectation_legal_status
        expectation_legal_status = request.form.getlist("expectation_legal_status")
        databaze.insert_expectation_legal_status(expectation_id, expectation_legal_status)
        # vyplni tabulku expectation_age
        expectation_age = request.form.getlist("expectation_age")
        databaze.insert_expectation_age(expectation_id, expectation_age)
        # vyplni tabulku expectation_anamnesis
        expectation_anamnesis_id = request.form.getlist("expectation_anamnesis_id")
        databaze.insert_expectation_anamnesis(expectation_id, expectation_anamnesis_id)
    return render_template("success.html")

@app.route('/search')
def search ():
    return render_template("search.html",
    )

@app.route('/search', methods=['POST'])
def search_post():
    if request.method == 'POST':
        approval_type_id = request.form.get("approval_type_id")
        legal_status_id= request.form.get("legal_status_id")
        district_id= request.form.get("district_id")
        age= request.form.get("child_age")
        sex= request.form.get("expectation_sex_id")
        sibling_info= request.form.get("siblings")
        physical_handicap= request.form.get("physical_handicap")
        mental_handicap= request.form.get("mental_handicap_id")
        ethnicity= request.form.get("ethnicity")
        anamnesis= request.form.get("anamnesis_id")
        expectation_table = databaze.tabulka_ku_search(approval_type_id, legal_status_id, district_id, age, sex, sibling_info, physical_handicap, mental_handicap,  ethnicity, anamnesis)
        print(expectation_table)
        return render_template("tabulka_search.html",
        expectation_table=expectation_table
        )

@app.route('/login')
def login ():
    return render_template("login.html",
    )

@app.route('/success')
def success ():
    return render_template("success.html",
    )

@app.route('/tabulka')
def tabulka_zobraz():
    family_table = databaze.tabulka_vypis()
    return render_template("tabulka.html", 
    family_table=family_table
    ) 

@app.route('/tabulka_ku')
def tabulka_ku ():
    expectation_table = databaze.tabulka_ku_vypis()
    print(expectation_table)
    return render_template("tabulka_ku.html",
    expectation_table=expectation_table,
    )

@app.route('/graf')
def graf():
    return render_template("graf.html")
    
@app.route("/graf-data")
def graf_data():
    description = {"kraj": ("string", "Kraj"),"volni": ("number", "Volni")}
    data = databaze.view_volni()
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table.ToJSon(columns_order=("kraj", "volni"), order_by="volni")

@app.route('/profil')
def profile ():
    return render_template("profil.html",)

@app.route('/profil/<int:family_id>', methods=['GET'])
def family_profile(family_id):
    family_profile = databaze.tabulka_ku_vypis_family(family_id)
    return render_template("profil.html",
    family_profile=family_profile,
    )

@app.route('/tabulka/<region_id>', methods=['GET'])
def table_region (region_id):
    family_table = databaze.table_region(region_id)
    print(family_table)
    return render_template("tabulka.html",
    family_table = family_table
    )


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    #app.logger.setLevel(gunicorn_logger.level)

