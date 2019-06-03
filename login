class User(UserMixin):
    def __init__(self, id, email, password_hash, role_id):
        self.id = id 
        self.email = email
        self.password_hash = password_hash
        self.role = role_id

def najdi_uzivatele(email):
    """ najde uzivatele v databazi """

    sql = """SELECT id_uzivatele, jmeno, prijmeni, email, heslo, telefon FROM uzivatele WHERE lower(email)=%s;"""
    conn = get_db()

    uzivatel = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (email.lower(),))
        # get the generated id back
        uzivatel = cur.fetchone()
        # close communication with the database
    finally:
        if conn is not None:
            conn.close()
    if uzivatel:
        return User(uzivatel[3], uzivatel[0], uzivatel[4], uzivatel[1], uzivatel[2],uzivatel[5])
    else:
        return None

@blueprint.route('/prihlaseni', methods=['GET', 'POST'])
def login():
    next = get_redirect_target()
    #print(next)
    form = LoginForm(request.form)

    if request.method == 'POST':
        # TODO: validace poli formulare??

        email = request.form["email"]
        heslo = request.form["heslo"]next
        uzivatel = najdi_uzivatele(email)
        # uspesne_prihlasen = False
        if uzivatel:
            if sha512(heslo.encode()).hexdigest() != uzivatel.password_hash:
                flash ('Špatně zadané heslo.', "danger")
            elif sha512(heslo.encode()).hexdigest() == uzivatel.password_hash:
                if login_user(uzivatel, force=True):
                    flash ('Uživatel byl úspěšně přihlášen.', "success")
                    if next.endswith('prihlaseni') or next.endswith('registrace'):
                        return redirect(url_for('zavody_bp.show_zavody'))
                    return redirect()
        if not uzivatel:
            flash ("Zadaný e-mail není v naší databázi. Nejprve se, prosím, zaregistruj.", "danger")
    return render_template('prihlaseni.html', form=form)

import currentuser
if cu je prihlaseny, tak, jinak