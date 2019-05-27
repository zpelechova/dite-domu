@app.route('/tabory', methods=["GET"])
def tabory():
    return render_template ("tabory.html")

select * from expectation
WHERE



@app.route('/search', methods=["POST"])
def search():
    print(request.form)

    if request.form.get("approval_type_id") == "1":
        approval_type_sql.append("approval_type_id = 1")
    if request.form.get("approval_type_id") == "2":
        approval_type_sql.append("approval_type_id = 2")
    podminky.append(" OR ".join(koho_sql))
    misto_sql_where = " OR ".join(misto_sql)
    
    zajmy_sql = ["1=1"]
    if request.form.get("camp_focus_classic") == "1":
        zajmy_sql.append("camp_focus_classic = 1")
    if request.form.get("camp_focus_language") == "1":
        zajmy_sql.append("camp_focus_language = 1")
    if request.form.get("camp_focus_sport") == "1":
        zajmy_sql.append("camp_focus_sport = 1")
    if request.form.get("camp_focus_art") == "1":
       zajmy_sql.append("camp_focus_art = 1")
    if request.form.get("camp_focus_christ") == "1":
        zajmy_sql.append("camp_focus_christ = 1")
    if request.form.get("camp_focus_science") == "1":
        zajmy_sql.append("camp_focus_science = 1")
    if request.form.get("camp_focus_others") == "1":
        zajmy_sql.append("camp_focus_others = 1")
    zajmy_sql_where = " OR ".join(zajmy_sql)

    misto_sql = ["1=1"]
    if request.form.get("camp_international") == "1":
        misto_sql.append("camp_international = 1")
    if request.form.get("camp_CR") == "1":
        misto_sql.append("camp_CR = 1")
    misto_sql_where = " OR ".join(misto_sql)

    typ_sql = ["1=1"]
    if request.form.get("camp_type_urban") == "1":
        typ_sql.append("camp_type_urban = 1")
    if request.form.get("camp_type_nature") == "1":
        typ_sql.append("camp_type_nature = 1")
    typ_sql_where = " OR ".join(typ_sql)

    vek_sql = ["1=1"]
    if request.form.get("age1") == "1":
        vek_sql.append("age1 = 1")
    if request.form.get("age2") == "1":
        vek_sql.append("age2 = 1")
    if request.form.get("age3") == "1":
        vek_sql.append("age3 = 1")
    if request.form.get("age4") == "1":
        vek_sql.append("age4 = 1")
    if request.form.get("age5") == "1":
        vek_sql.append("age5 = 1")
    vek_sql_where = " OR ".join(vek_sql)

    delka_sql = ["1=1"]
    if request.form.get("stay_day") == "1":
        delka_sql.append("stay_day = 1")
    if request.form.get("stay_weekend") == "1":
        delka_sql.append("stay_weekend = 1")
    if request.form.get("stay_week") == "1":
       delka_sql.append("stay_week = 1")
    if request.form.get("stay_more") == "1":
        delka_sql.append("stay_more = 1")
    if request.form.get("stay_2weeks") == "1":
        delka_sql.append("stay_2weeks = 1")
    delka_sql_where = " OR ".join(delka_sql)

    cena = request.form.get("camp_price")
    if cena == "price_to":
        cena_sql = "camp_price <= 2000"
    else:
        cena_sql = "camp_price > 2000"
    podminky.append(cena_sql)

    
    termin_start = request.form.get("date_from")
    termin_finish = request.form.get("date_to")
    termin_sql = ["1=1"]
    if termin_start:
        termin_sql.append("camp_date_start >= '" + termin_start + "'")
    if termin_finish:
        termin_sql.append("camp_date_finish <= '" + termin_finish + "'")
    termin_sql_where = " AND ".join(termin_sql)
    podminky.append(termin_sql_where)

    where = "(" + ") AND (".join(podminky) + ")"

    sql = """SELECT * FROM camp WHERE  (""" + where + ")"
    print(sql)
    
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return render_template ("tabory_vysledky.html", tabory_z_db = data)



@app.route('/tabor/<id_taboru>')
def tabor_detail(id_taboru):

    conn = db.get_db()
    sql = """SELECT * FROM camp WHERE camp_id = %s"""
    cur = conn.cursor()
    cur.execute(sql, (id_taboru, ))
    data = cur.fetchall()

    return render_template("tabor_detail.html", tabor_z_db = data)