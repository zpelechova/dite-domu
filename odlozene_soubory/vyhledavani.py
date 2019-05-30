from flask import request
import psycopg2
import psycopg2.extras


try:
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    cursor = connection.cursor()
    appr_type = request.form["approval_type_id"]
    print(1)
    sql = """SELECT * FROM public.family WHERE approval_type_id = ?"""
    print(sql)
    cursor.execute(sql, (appr_type,))
    res = cursor.fetchall()
    print(res)
    # for r in res:
    #   print(r['approval_type'])
except (Exception, psycopg2.Error) as error :
    print ("PostgreSQL Exception", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
