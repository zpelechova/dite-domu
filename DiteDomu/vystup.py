import psycopg2
import psycopg2.extras
# psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor
# pak budou všechny kurzory toho připojení (vytvořené voláním `conn.cursor`) mít jednotlivé řádky jako slovník


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    #vypise vsechny verejne udaje z tabulky family,
    query="""SELECT file_number, at.name AS approval_type, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id
            FROM public.family as f
            LEFT JOIN public.approval_type AS at ON f.approval_type_id = at.id
            ORDER BY region_id;"""
	##WHERE xxx AND id_zavod=%s znamena ze vyberea data pro nejaky zavod, ktery zvolil uzivatel
# spusteni query
    cursor.execute(query)
    res = cursor.fetchall()
    print(res)
    # for r in res:
    #   print(r['approval_type'])

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