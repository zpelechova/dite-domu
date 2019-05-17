import psycopg2
import psycopg2.extras
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

def insert_parent(family_id, sex_id, year_of_birth):
    """ vyplni tabulku family_parent """
    sql = """INSERT INTO public.family_parent
            (family_id, sex_id, year_of_birth)
             VALUES(%s, %s, %s) RETURNING id;"""
    conn = get_db()
    family_parent_id = None
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (family_id, sex_id, year_of_birth))
        # get the generated id back
        family_parent_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
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
        # execute the INSERT statement
        cur.execute(sql, (family_id, sex_id, year_of_birth, relationship_id))
        # get the generated id back
        child_in_care_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return child_in_care_id

def return_family():
    """ Vypise polozky tabulky family. """
    sql = """SELECT file_number, approval_type_id, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse FROM public.family"""
    conn = get_db()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute(sql)
    vyber_z_databaze = cur.fetchall()
    conn.close()
    return vyber_z_databaze    
