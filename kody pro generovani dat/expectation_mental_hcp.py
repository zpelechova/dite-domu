import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_mental_handicap"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    
    cursor.execute("truncate expectation_mental_handicap cascade")
    cursor.execute("ALTER SEQUENCE expectation_mental_handicap_id_seq RESTART")
    
    for i in range(1, 201):
        # definice sloupcu
        # cyklus na nahodne vybirani multiple choice (1-2)
        expectation_id = i
        num_ments = random.randint(1, 2)
        ment_ids = []
        while len(ment_ids) < num_ments:
            ment_id = random.randint(1, 2)
            if ment_id not in ment_ids:
                ment_ids.append(ment_id)
        
        for mental_handicap_id in ment_ids:
            # definice query
            #DANOVA VERZE
            query ="""INSERT INTO public.expectation_mental_handicap(expectation_id, mental_handicap_id)VALUES(%s, %s);"""
    
    
        # spusteni query
        cursor.execute(query,(expectation_id, mental_handicap_id))

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