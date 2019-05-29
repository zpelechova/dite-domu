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
        # execute the INSERT statement
        cur.execute(sql, (email, password, "2", datetime.datetime.now(), 1))
        # get the generated id back
        id_uzivatele = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        flash('Vaše emailová adresa už je v naší databázi.')
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_uzivatele

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_uzivatele

def insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care):
    """ vyplni tabulku family """
    sql = """INSERT INTO public.family
            (file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    family_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date, number_child_in_care))
        family_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return family_id

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return family_parent_id

def insert_child_in_care(family_id, sex_id, year_of_birth, relationship_id):
    """ vyplni tabulku child_in_care"""
    sql = """INSERT INTO public.child_in_care
            (family_id, sex_id, year_of_birth, relationship_id)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    child_in_care_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (family_id, sex_id, year_of_birth, relationship_id))
        child_in_care_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return child_in_care_id

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return expectation_id

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
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

def tabulka_vypis():
    sql = """SELECT f.id
                    , rg.name as region
                    , ds.name as district
                    , es.name as expectation_status
                    , ap.name as approval_type
                    , ca.name as carer_info
                    , f.prepcourse
                    FROM public.family as f
                    LEFT JOIN public.region AS rg ON f.region_id = rg.id 
                    LEFT JOIN public.district AS ds ON f.district_id = ds.id 
                    LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id 
                    LEFT JOIN public.approval_type AS ap ON f.approval_type_id = ap.id 
                    LEFT JOIN public.carer_info AS ca ON f.carer_info_id = ca.id 
                    ORDER BY f.id DESC"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        family_table = cur.fetchall()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return family_table

def tabulka_ku_vypis():
    sql = """SELECT family_id,
                    string_agg(distinct ag.name, ', ') AS expectation_age,
                    string_agg(distinct s.name , ', ') AS expectation_sex,
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
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return expectation_table

def view_volni():
    sql = """SELECT * FROM view_volni_final ORDER BY volni"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        view_volni = cur.fetchall()
        conn.close()
        description = {"kraj": ("string", "Kraj"),
               "volni": ("number", "Volni")}
        data = view_volni
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        # print "Content-type: text/plain"
        # print
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return view_volni

def get_expectation_ages(family_id):
    sql = """select age.name
              from expectation_age
              join expectation on expectation.Id = expectation_age.expectation_id
              join age on age.Id = expectation_age.age_id
              where family_id = %s"""
    conn = get_db()
    try:
        #cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) - Uprava Lukas, bez Real Dictionary
        cur = conn.cursor()
        cur.execute(sql, family_id)
        result = cur.fetchall()
    return result
      
def tabulka_ku_search(approval_type_id, legal_status_id, district_id, age, sex, sibling_info, physical_handicap, mental_handicap,  ethnicity, anamnesis):
    expectation_table = []
    sql = """SELECT * 
                FROM public.expectation e
                LEFT JOIN public.family f ON e.family_id = f.id
                WHERE (%(approval_type_id)s IS NULL OR approval_type_id = %(approval_type_id)s)
                  AND (%(sex)s IS NULL OR sex_id = %(sex)s OR sex_id = 3)
                """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql, {"approval_type_id": approval_type_id, 
                          "sex": sex})
        expectation_table = cur.fetchall()
        print(expectation_table)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return expectation_table
