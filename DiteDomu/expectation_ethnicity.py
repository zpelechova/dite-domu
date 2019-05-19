import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_ethnicity"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    #????myslim neni nutne, vyprazdneni tabulek je u account tab
    cursor.execute("truncate expectation_ethnicity cascade")
    cursor.execute("ALTER SEQUENCE expectation_ethnicity_id_seq RESTART")
    for i in range(1, 19):
        # definice sloupcu
        # cyklus na nahodne vybirani multiple choice u ethnicity (1-4)
        expectation_id = i
        num_eths = random.randint(1, 4)
        eth_ids = []
        while len(eth_ids) < num_eths:
            eth_id = random.randint(1, 4)
            if eth_id not in eth_ids:
                eth_ids.append(eth_id)
        
        for ethnicity_id in eth_ids:
            # definice query
            #DANOVA VERZE
            query ="""INSERT INTO public.expectation_ethnicity(expectation_id, ethnicity_id)VALUES(%s, %s);"""
            # query ="INSERT INTO public.expectation_ethnicity(expectation_id, ethnicity_id)VALUES("+str(expectation_id)+","+ str(ethnicity_id) + ");" LUKASOVO VERZE
            # spusteni query
            cursor.execute(query, (expectation_id, ethnicity_id))

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