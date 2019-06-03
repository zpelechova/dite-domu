import psycopg2
import psycopg2.extras

try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    #vypise vsechny verejne udaje z tabulky family,
    query="""SELECT file_number, note, prepcourse, approval_date, at.name AS approval_type, ro.name AS regional_office, es.name AS expectation_status, r.name AS region, d.name AS district, ci.name AS carer_info FROM public.family as f LEFT JOIN public.approval_type AS at ON f.approval_type_id = at.id LEFT JOIN public.regional_office AS ro ON f.regional_office_id = ro.id LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id LEFT JOIN public.region AS r ON f.region_id = r.id LEFT JOIN public.district AS d ON f.district_id = d.id LEFT JOIN public.carer_info AS ci ON f.carer_info_id = ci.id ORDER BY region_id;"""
	##WHERE xxx AND id_zavod=%s znamena ze vyberea data pro nejaky zavod, ktery zvolil uzivatel
# spusteni query
    cursor.execute(query)
    res = cursor.fetchall()
    print(res)
    approval_type = [(r['approval_type']) for r in res]
    print(approval_type)
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