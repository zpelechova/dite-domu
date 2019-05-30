import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_anamnesis"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    
    cursor.execute("truncate expectation_anamnesis cascade")
    cursor.execute("ALTER SEQUENCE expectation_anamnesis_id_seq RESTART")
    
    for i in range(1, 501):
        # definice sloupcu
        # cyklus na nahodne vybirani multiple choice u anamnesis (1-7)
        expectation_id = i
        num_anams = random.randint(1, 7)
        anam_ids = []
        while len(anam_ids) < num_anams:
            anam_id = random.randint(1, 7)
            if anam_id not in anam_ids:
                anam_ids.append(anam_id)
        
        for anamnesis_id in anam_ids:
            # definice query
           
            query ="""INSERT INTO public.expectation_anamnesis(expectation_id, anamnesis_id)VALUES(%s, %s);"""
            
            # spusteni query
            cursor.execute(query, (expectation_id, anamnesis_id))
        
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