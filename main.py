# Z flasku naimportuje spoustu různých funkcí, které budeme potřebovat
from flask import Blueprint, render_template
import db_funkce


# Vytvoří nový blueprint s názvem "about_bp" a uloží ho to proměnné blueprint
blueprint = Blueprint('registrace_nr_bp', __name__)

# Zaregistruje funkci show_about() jako funkci, kterou má Flask zavolat, když 
# uživatel otevře v prohlížeči stránku "/about"
@blueprint.route('/registrace_nr')
def show_about():
    # Zavolá funkci render_template(), která vezme template about.html a
    # vygeneruje výsledné HTML, které vrátí jako výsledek z téhle funkce zpátky
    # do Fasku, a ten ji pošle k uživateli do prohlížeče.
    return render_template('registrace_nr.html')


@blueprint.route('/')
def show_index():
    return render_template('index.html')