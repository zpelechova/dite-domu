import psycopg2
import datetime
import os
import hashlib, binascii
from flask import g, flash
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
        # execute the INSERT statement
        cur.execute(sql, (first_name, last_name, position_name, email, password, phone, "3", datetime.datetime.now(), 2))
        # get the generated id back
        id_uzivatele = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return id_uzivatele

# def accounts():
#     """ Vypise seznam uživatelů na webu v klesajicim poradi. """
#     sql = """SELECT * FROM public.account ORDER BY id DESC"""
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(sql)
#     data = cur.fetchall()
#     conn.close()
#     return data

# def account(account_id):
#     """ Vypise seznam uživatelů na webu v klesajicim poradi. """
#     sql = """SELECT * FROM public.account WHERE id=%s ORDER BY id DESC"""
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(sql,account_id)
#     datas = cur.fetchall()
#     conn.close()
#     return datas

def insert_family(file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id):
    """ vyplni tabulku family """
    sql = """INSERT INTO public.family
            (file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    family_id = None
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id))
        # get the generated id back
        family_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return family_id


# def insert_expectation(family_id, sex_id):
#     """ vlozi do tabulky expectation id family a sex """
#     sql = """INSERT INTO public.expectation
#             (family_id, sex_id)
#              VALUES(%s, %s) RETURNING id;"""
#     conn = get_db()
#     id_expectation = None
#     try:
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (family_id, sex_id))
#         # get the generated id back
#         id_expectation = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#     return id_expectation

# def show_email():
#     """ Vypise email prave registrovaneho uzivatele. """
#     sql = """SELECT email FROM public.account ORDER BY id DESC limit 1"""
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(sql)
#     show_email = cur.fetchone()
#     conn.close()
#     return show_email
# print(show_email)

def show_district():
    """ Vypise uživatele a okres, kde bydlí, taková zkouška. """
    sql = """SELECT district.name AS okres, family.prepcourse AS pripravka, account.id as uzivatel 
    FROM district JOIN family ON district.id = family.district_id JOIN account ON family.account_id = account.id
    ORDER BY account.id DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    districts = cur.fetchall()
    conn.close()
    return districts