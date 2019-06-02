import gviz_api
import psycopg2
import psycopg2.extras
import datetime
import os
import hashlib, binascii
from flask import g, flash, request
from hashlib import sha512
from flask_login import UserMixin
from functools import lru_cache

def get_db():
    """ Spojeni s dtb. """
    if not hasattr(g, 'db') or g.db.closed == 1:
		# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require')
        g.db = con
    return g.db

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def registrace_nr(email, password):
    """ vlozi novou nahradni rodinu do databaze """
    sql = """INSERT INTO public.account
            (email, password, role_id, created_on, account_status_id)
             VALUES(%s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    id_uzivatele = None
    password = hash_password(password)
    try:
        cur = conn.cursor()
        cur.execute(sql, (email, password, "2", datetime.datetime.now(), 1))
        id_uzivatele = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return id_uzivatele
    finally:
        if conn is not None:
            conn.close()

def registrace_ku(first_name, last_name, position_name, email, password, phone):
    """ vlozi noveho pracovnika KU do databaze """
    sql = """INSERT INTO public.account
            (officer_first_name, officer_last_name, officer_position_name, email, password, telephone, role_id, created_on, account_status_id)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    id_uzivatele = None
    password = hash_password(password)  
    try:
        cur = conn.cursor()
        cur.execute(sql, (first_name, last_name, position_name, email, password, phone, "3", datetime.datetime.now(), 2))
        id_uzivatele = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return id_uzivatele
    finally:
        if conn is not None:
            conn.close()

def insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care):
    """ vyplni tabulku family """
    sql = """INSERT INTO public.family
            (file_number, approval_type_id, regional_office_id, expectation_status_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    family_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (file_number, approval_type_id, regional_office_id, expectation_status_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care))
        family_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return family_id
    finally:
        if conn is not None:
            conn.close()

def insert_parent1(family_id, parent1_sex_id, parent1_year_of_birth):
    """ vyplni tabulku family_parent pro prdvniho rodice"""
    sql = """INSERT INTO public.family_parent
            (family_id, sex_id, year_of_birth)
             VALUES(%s, %s, %s) RETURNING id;"""
    conn = get_db()
    family_parent_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (family_id, parent1_sex_id, parent1_year_of_birth))
        family_parent_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return family_parent_id
    finally:
        if conn is not None:
            conn.close()

def insert_child_in_care(family_id, youngest_child_sex_id, youngest_child_year_of_birth, relationship_id):
    """ vyplni tabulku child_in_care"""
    sql = """INSERT INTO public.child_in_care
            (family_id, sex_id, year_of_birth, relationship_id)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    child_in_care_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (family_id, youngest_child_sex_id, youngest_child_year_of_birth, relationship_id))
        child_in_care_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return child_in_care_id
    finally:
        if conn is not None:
            conn.close()

def insert_expectation(family_id, sex_id):
    """ vyplni tabulku expectation"""
    sql = """INSERT INTO public.expectation
            (family_id, sex_id)
             VALUES(%s, %s) RETURNING id;"""
    conn = get_db()
    expectation_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (family_id, sex_id))
        expectation_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return expectation_id
    finally:
        if conn is not None:
            conn.close()

def insert_expectation_sibling_info(expectation_id, sibling_info_id):
    """ vyplni tabulku expectation"""
    for x in sibling_info_id:
            sql = """INSERT INTO public.expectation_sibling_info
                (expectation_id, sibling_info_id)
                VALUES(%s, %s);"""
            conn = get_db()
            try:
                cur = conn.cursor()
                cur.execute(sql, (expectation_id, x))
                conn.commit()
                cur.close()
            finally:
                if conn is not None:
                    conn.close()

def insert_expectation_mental_handicap(expectation_id, mental_handicap_id):
    """ vyplni tabulku expectation_mental_handicap"""
    sql = """INSERT INTO public.expectation_mental_handicap
            (expectation_id, mental_handicap_id)
             VALUES(%s, %s);"""
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(sql, (expectation_id, mental_handicap_id))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

def insert_expectation_physical_handicap(expectation_id, physical_handicap_id):
    """ vyplni tabulku expectation_physical_handicap"""
    sql = """INSERT INTO public.expectation_physical_handicap
            (expectation_id, physical_handicap_id)
             VALUES(%s, %s) RETURNING id;"""
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(sql, (expectation_id, physical_handicap_id))
        conn.commit()
        cur.close()
    finally:
        if conn is not None:
            conn.close()

def insert_expectation_legal_status(expectation_id, legal_status_id):
    """ vyplni tabulku expectation_legal_status"""
    for x in legal_status_id:
        sql = """INSERT INTO public.expectation_legal_status
                (expectation_id, legal_status_id)
                VALUES(%s, %s);"""
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute(sql, (expectation_id, x))
            conn.commit()
            cur.close()
        finally:
            if conn is not None:
                conn.close()

def insert_expectation_age(expectation_id, age_id):
    """ vyplni tabulku expectation_age """
    for x in age_id:
        sql = """INSERT INTO public.expectation_age
                (expectation_id, age_id)
                VALUES(%s, %s);"""
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute(sql, (expectation_id, x))
            conn.commit()
            cur.close()
        finally:
            if conn is not None:
                conn.close()

def insert_expectation_anamnesis(expectation_id, anamnesis_id):
    """ vyplni tabulku expectation_anamnesis"""
    for x in anamnesis_id:
        sql = """INSERT INTO public.expectation_anamnesis
                (expectation_id, anamnesis_id)
                VALUES(%s, %s);"""
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute(sql, (expectation_id, x))
            conn.commit()
            cur.close()
        finally:
            if conn is not None:
                conn.close()

def insert_expectation_ethnicity(expectation_id, ethnicity_id):
    """ vyplni tabulku expectation_ethnicity"""
    for x in ethnicity_id:
        sql = """INSERT INTO public.expectation_ethnicity
                (expectation_id, ethnicity_id)
                VALUES(%s, %s);"""
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute(sql, (expectation_id, x))
            conn.commit()
            cur.close()
        finally:
            if conn is not None:
                conn.close()

def tabulka_vypis():
# zobrazí tabulku "přehled volných rodin"
    sql = """SELECT f.id
                    , ds.name as district
                    , rg.name as region
                    , es.name as expectation_status
                    , ap.name as approval_type
                    , ca.name as carer_info
                    , f.prepcourse
                    FROM public.family as f
                    LEFT JOIN public.district AS ds ON f.district_id = ds.id 
                    LEFT JOIN public.region AS rg ON ds.region_id = rg.id 
                    LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id 
                    LEFT JOIN public.approval_type AS ap ON f.approval_type_id = ap.id 
                    LEFT JOIN public.carer_info AS ca ON f.carer_info_id = ca.id 
                    WHERE f.expectation_status_id = 1
                    ORDER BY f.id DESC"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        family_table = cur.fetchall()
        conn.close()
        return family_table
    finally:
        if conn is not None:
            conn.close()

def table_region(region_id):
# zobrazí tabulku "přehled volných rodin v daném kraji"
    sql = """SELECT f.id
                    , ds.name as district
                    , rg.name as region
                    , es.name as expectation_status
                    , ap.name as approval_type
                    , ca.name as carer_info
                    , f.prepcourse
                    FROM public.family as f
                    LEFT JOIN public.district AS ds ON f.district_id = ds.id 
                    LEFT JOIN public.region AS rg ON ds.region_id = rg.id 
                    LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id 
                    LEFT JOIN public.approval_type AS ap ON f.approval_type_id = ap.id 
                    LEFT JOIN public.carer_info AS ca ON f.carer_info_id = ca.id 
                    WHERE rg.id = %s AND f.expectation_status_id = 1
                    ORDER BY f.id DESC"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (region_id, ))
        family_table = cur.fetchall()
        print(family_table)
        conn.close()
        return family_table
    finally:
        if conn is not None:
            conn.close()

def tabulka_ku_vypis():
# zobrazí tabulku "Výpis pro KU" bez filtrovaných parametrů
    sql = """SELECT family_id,
                    string_agg(distinct ag.name, ', ') AS expectation_age,
                    string_agg(distinct s.name_child , ', ') AS expectation_sex,
                    string_agg(distinct sb.name , ', ') AS expectation_sibling_info,
                    string_agg(distinct ph.name , ', ') AS expectation_physical_handicap,
                    string_agg(distinct mh.name , ', ') AS expectation_mental_handicap,
                    string_agg(distinct et.name , ', ') AS expectation_ethnicity,
                    string_agg(distinct an.name , ', ') AS expectation_anamnesis,
                    string_agg(distinct ls.name , ', ') AS expectation_legal_status
                    FROM public.expectation as e
                    LEFT JOIN public.expectation_age AS ea ON e.id = ea.expectation_id 
                    LEFT JOIN public.age AS ag ON ea.age_id = ag.id
                    LEFT JOIN public.expectation_anamnesis AS ean ON e.id = ean.expectation_id 
                    LEFT JOIN public.anamnesis AS an ON ean.anamnesis_id = an.id
                    LEFT JOIN public.expectation_ethnicity AS eet ON e.id = eet.expectation_id 
                    LEFT JOIN public.ethnicity AS et ON eet.ethnicity_id = et.id
                    LEFT JOIN public.expectation_legal_status AS els ON e.id = els.expectation_id 
                    LEFT JOIN public.legal_status AS ls ON els.legal_status_id = ls.id
                    LEFT JOIN public.expectation_mental_handicap AS emh ON e.id = emh.expectation_id 
                    LEFT JOIN public.mental_handicap AS mh ON emh.mental_handicap_id = mh.id
                    LEFT JOIN public.expectation_physical_handicap AS eph ON e.id = eph.expectation_id 
                    LEFT JOIN public.physical_handicap AS ph ON eph.physical_handicap_id = ph.id
                    LEFT JOIN public.expectation_sibling_info AS esb ON e.id = esb.expectation_id 
                    LEFT JOIN public.sibling_info AS sb ON esb.sibling_info_id = sb.id
                    LEFT JOIN public.sex AS s ON e.sex_id = s.id
                    GROUP BY e.family_id
                    ORDER BY family_id desc"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        expectation_table = cur.fetchall()
        return expectation_table
    finally:
        if conn is not None:
            conn.close()

def tabulka_ku_search(approval_type_id, legal_status_id, district_id, age, sex, sibling_info, physical_handicap, mental_handicap,  ethnicity, anamnesis):
# zobrazí tabulku "Výpis pro KU" na základě zadaných parametrů
    sql = """
    WITH a AS (SELECT 
    f.id AS family_id,
    ag.name AS expectation_age,
    s.name_child AS expectation_sex,
    sb.name AS expectation_sibling_info,
    ph.name AS expectation_physical_handicap,
    mh.name AS expectation_mental_handicap,
    et.name AS expectation_ethnicity,
    an.name AS expectation_anamnesis,
    ls.name AS expectation_legal_status,
    rg.name AS region,
    ds.name AS district,
    es.name AS expectation_status,
    ap.name AS approval_type,
    ca.name AS carer_info,
    f.prepcourse,
    CASE WHEN (%(approval_type_id)s IS NULL OR approval_type_id = %(approval_type_id)s) THEN 1 ELSE 0 END AS case_approval
    , CASE WHEN (%(sex)s IS NULL OR sex_id = %(sex)s OR sex_id = 3) THEN 1 ELSE 0 END AS case_sex
    , CASE WHEN (%(legal_status_id)s IS NULL OR legal_status_id = %(legal_status_id)s) THEN 1 ELSE 0 END AS case_legal_status
    , CASE WHEN (%(district_id)s IS NULL OR district_id = %(district_id)s OR district_id = 78) THEN 1 ELSE 0 END AS case_district
    , CASE WHEN (%(age)s IS NULL OR age_id = %(age)s) THEN 1 ELSE 0 END AS case_age
    , CASE WHEN (%(siblings)s IS NULL OR esb.sibling_info_id = %(siblings)s) THEN 1 ELSE 0 END AS case_siblings
    , CASE WHEN (%(physical_handicap)s IS NULL OR physical_handicap_id = %(physical_handicap)s) THEN 1 ELSE 0 END AS case_physical_handicap
    , CASE WHEN (%(mental_handicap)s IS NULL OR mental_handicap_id = %(mental_handicap)s) THEN 1 ELSE 0 END AS case_mental_handicap
    , CASE WHEN (%(ethnicity)s IS NULL OR ethnicity_id = %(ethnicity)s) THEN 1 ELSE 0 END AS case_ethnicity
    , CASE WHEN (%(anamnesis)s IS NULL OR anamnesis_id = %(anamnesis)s) THEN 1 ELSE 0 END AS case_anamnesis
    FROM public.family as f
    LEFT JOIN public.expectation as e ON f.id = e.family_id
    LEFT JOIN public.expectation_age AS ea ON e.id = ea.expectation_id 
    LEFT JOIN public.age AS ag ON ea.age_id = ag.id
    LEFT JOIN public.expectation_anamnesis AS ean ON e.id = ean.expectation_id 
    LEFT JOIN public.anamnesis AS an ON ean.anamnesis_id = an.id
    LEFT JOIN public.expectation_ethnicity AS eet ON e.id = eet.expectation_id 
    LEFT JOIN public.ethnicity AS et ON eet.ethnicity_id = et.id
    LEFT JOIN public.expectation_legal_status AS els ON e.id = els.expectation_id 
    LEFT JOIN public.legal_status AS ls ON els.legal_status_id = ls.id
    LEFT JOIN public.expectation_mental_handicap AS emh ON e.id = emh.expectation_id 
    LEFT JOIN public.mental_handicap AS mh ON emh.mental_handicap_id = mh.id
    LEFT JOIN public.expectation_physical_handicap AS eph ON e.id = eph.expectation_id 
    LEFT JOIN public.physical_handicap AS ph ON eph.physical_handicap_id = ph.id
    LEFT JOIN public.expectation_sibling_info AS esb ON e.id = esb.expectation_id 
    LEFT JOIN public.sibling_info AS sb ON esb.sibling_info_id = sb.id
    LEFT JOIN public.sex AS s ON e.sex_id = s.id
    LEFT JOIN district ds ON f.district_id = ds.id
    LEFT JOIN region rg ON ds.region_id = rg.id
    LEFT JOIN expectation_status es ON f.expectation_status_id = es.id
    LEFT JOIN approval_type ap ON f.approval_type_id = ap.id
    LEFT JOIN carer_info ca ON f.carer_info_id = ca.id
    WHERE f.expectation_status_id = 1),
	b AS (SELECT *, (case_approval + case_sex + case_legal_status + case_district + case_age + case_siblings + case_physical_handicap + case_mental_handicap + case_ethnicity + case_anamnesis) AS result,
    ROW_NUMBER() OVER(
    PARTITION BY family_id
    ORDER BY (case_approval + case_sex + case_legal_status + case_district + case_age + case_siblings + case_physical_handicap + case_mental_handicap + case_ethnicity + case_anamnesis) DESC) AS poradi
	FROM a)
	SELECT * FROM b
	WHERE poradi = 1 AND result > 7
    ORDER BY result DESC
    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, {"approval_type_id": approval_type_id, 
                        "sex": sex,
                        "legal_status_id": legal_status_id ,
                        "district_id": district_id ,
                        "age": age ,
                        "siblings": sibling_info ,
                        "physical_handicap": physical_handicap ,
                        "mental_handicap": mental_handicap ,
                        "ethnicity": ethnicity ,
                        "anamnesis": anamnesis ,
                        })
        expectation_table = cur.fetchall()
        print(expectation_table)
        return expectation_table
    finally:
        if conn is not None:
            conn.close()

def tabulka_ku_vypis_family(family_id):
# zobrazí tabulku "Profil"
    sql = """ 
SELECT f.id AS family_id,
file_number,
approval_date,
prepcourse,
note,
number_child_in_care,
ap.name AS approval_type,
ro.name AS regional_office,
es.name AS expectation_status,
ds.name AS district,
s2.name_child as youngest_child_sex, 
rl.name AS youngest_child_relationship, 
cc.year_of_birth AS youngest_child_year_of_birth,
ci.name AS carer_info,
string_agg(DISTINCT s3.name_adult, ',') AS parent_sex, 
string_agg(DISTINCT fp.year_of_birth::text, ',') AS parent_year_of_birth,
string_agg(distinct ag.name, ', ') AS expectation_age,
string_agg(distinct s.name_child , ', ') AS expectation_sex,
string_agg(distinct sb.name , ', ') AS expectation_sibling_info,
string_agg(distinct ph.name , ', ') AS expectation_physical_handicap,
string_agg(distinct mh.name , ', ') AS expectation_mental_handicap,
string_agg(distinct et.name , ', ') AS expectation_ethnicity,
string_agg(distinct an.name , ', ') AS expectation_anamnesis,
string_agg(distinct ls.name , ', ') AS expectation_legal_status
FROM family as f
LEFT JOIN public.expectation AS e ON f.id = e.family_id
LEFT JOIN public.expectation_age AS ea ON e.id = ea.expectation_id 
LEFT JOIN public.age AS ag ON ea.age_id = ag.id
LEFT JOIN public.expectation_anamnesis AS ean ON e.id = ean.expectation_id 
LEFT JOIN public.anamnesis AS an ON ean.anamnesis_id = an.id
LEFT JOIN public.expectation_ethnicity AS eet ON e.id = eet.expectation_id 
LEFT JOIN public.ethnicity AS et ON eet.ethnicity_id = et.id
LEFT JOIN public.expectation_legal_status AS els ON e.id = els.expectation_id 
LEFT JOIN public.legal_status AS ls ON els.legal_status_id = ls.id
LEFT JOIN public.expectation_mental_handicap AS emh ON e.id = emh.expectation_id 
LEFT JOIN public.mental_handicap AS mh ON emh.mental_handicap_id = mh.id
LEFT JOIN public.expectation_physical_handicap AS eph ON e.id = eph.expectation_id 
LEFT JOIN public.physical_handicap AS ph ON eph.physical_handicap_id = ph.id
LEFT JOIN public.expectation_sibling_info AS esb ON e.id = esb.expectation_id 
LEFT JOIN public.sibling_info AS sb ON esb.sibling_info_id = sb.id
LEFT JOIN public.sex AS s ON e.sex_id = s.id
LEFT JOIN public.approval_type AS ap ON f.approval_type_id = ap.id
LEFT JOIN public.regional_office AS ro ON f.regional_office_id = ro.id
LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id
LEFT JOIN public.district AS ds ON f.district_id = ds.id
LEFT JOIN public.child_in_care AS cc ON cc.family_id = f.id
LEFT JOIN public.relationship AS rl ON cc.relationship_id = rl.id
LEFT JOIN public.sex AS s2 ON cc.sex_id = s2.id
LEFT JOIN public.carer_info AS ci ON f.carer_info_id = ci.id
LEFT JOIN public.family_parent AS fp ON fp.family_id = f.id
LEFT JOIN public.sex AS s3 ON fp.sex_id = s3.id
WHERE f.id = %s
GROUP BY f.id, file_number, approval_date, prepcourse, note, number_child_in_care, ap.name, ro.name, es.name, ds.name, s2.name_child, rl.name, cc.year_of_birth, ci.name
"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, (family_id,))
        family_profile = cur.fetchone()
        print(family_profile)
        return family_profile
    finally:
        if conn is not None:
            conn.close()

def volni():
    sql = """SELECT * FROM volni"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        volni = cur.fetchall()
        conn.close()
        description = {"kraj": ("string", "Kraj"),
               "osvojitele": ("number", "Osvojitelé"),
               "pestouni": ("number", "Pěstouni")}
        data = volni
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        return volni
    finally:
        if conn is not None:
            conn.close()
