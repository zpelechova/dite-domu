import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")

    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_legal_status"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    cursor.execute("truncate expectation_legal_status cascade")
    cursor.execute("ALTER SEQUENCE expectation_legal_status_id_seq RESTART")

    # for i in range(1, 20):
    #     # definice sloupcu
    #     legal_status_id = random.randint(1,4)
    #     # definice query
    #     query = "INSERT INTO public.expectation_legal_status(family_id,legal_status_id)VALUES("+str(family_id)+","+ str(legal_status_id) + ");"
    #     # spusteni query
    #     cursor.execute(query)
    for i in range(1, 501):
        # definice sloupcu
        # cyklus na nahodne vybirani multiple choice u legal_status (1-4)
        expectation_id = i
        num_legals = random.randint(1, 4)
        legal_ids = []
        while len(legal_ids) < num_legals:
            legal_id = random.randint(1, 4)
            if legal_id not in legal_ids:
                legal_ids.append(legal_id)

        for legal_status_id in legal_ids:
            # definice query
            #DANOVA VERZE
            query ="""INSERT INTO public.expectation_legal_status(expectation_id, legal_status_id)VALUES(%s, %s);"""

            # spusteni query
            cursor.execute(query, (expectation_id, legal_status_id))
    connection.commit()

# v pripade databazove chyby, vyhodit chybu
except (Exception, psycopg2.Error) as error :
    print ("PostgreSQL Exception", error)
# uzavreni databazoveho pripojeni
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")