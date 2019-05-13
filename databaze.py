import psycopg2
import datetime
import os
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

def registrace_nr(email, password):
    """ vlozi novou nahradni rodinu do databaze """
    sql = """INSERT INTO public.account
            (email, password, role_id, created_on, account_status_id)
             VALUES(%s, %s, %s, %s, %s) RETURNING id;"""
    conn = get_db()
    id_uzivatele = None
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

def accounts():
    """ Vypise seznam uživatelů na webu v klesajicim poradi. """
    sql = """SELECT * FROM public.account ORDER BY id DESC"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data

# def account(account_id):
#     """ Vypise seznam uživatelů na webu v klesajicim poradi. """
#     sql = """SELECT * FROM public.account WHERE id=%s ORDER BY id DESC"""
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute(sql,account_id)
#     datas = cur.fetchall()
#     conn.close()
#     return datas
