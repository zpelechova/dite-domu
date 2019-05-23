import psycopg2
import psycopg2.extras
import gviz_api

try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #vypise vsechny verejne udaje z tabulky family,
    query="""SELECT * FROM view_volni_final;"""
	##WHERE xxx AND id_zavod=%s znamena ze vyberea data pro nejaky zavod, ktery zvolil uzivatel
# spusteni query
    cursor.execute(query)
    data = cursor.fetchall()
    # print(data)
    # approval_type = [(r['approval_type']) for r in res]
    # print(approval_type)
# v pripade databazove chyby, vyhodit chybu
except (Exception, psycopg2.Error) as error :
    print ("PostgreSQL Exception", error)
# uzavreni databazoveho pripojeni
finally:
    # close communication with the database
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

description = {"kraj": ("string", "Kraj"),
               "volni": ("number", "Volni")}
data = data
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)
# print "Content-type: text/plain"
print
print(data_table.ToJSonResponse(columns_order=("kraj", "volni"),
                                order_by="volni"))
