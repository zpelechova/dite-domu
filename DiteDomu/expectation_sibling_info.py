import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_sibling_info"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    #????myslim neni nutne, vyprazdneni tabulek je u account tab
    cursor.execute("truncate expectation_sibling_info cascade")
    cursor.execute("ALTER SEQUENCE expectation_sibling_info_id_seq RESTART")
    for i in range(1, 501):
        # definice sloupcu
        # cyklus na nahodne vybirani multiple choice u sibling_info (1-4)
        expectation_id = i
        num_sibls = random.randint(1, 4)
        sibl_ids = []
        while len(sibl_ids) < num_sibls:
            sibl_id = random.randint(1, 4)
            if sibl_id not in sibl_ids:
                sibl_ids.append(sibl_id)
        
        for sibling_info_id in sibl_ids:
            # definice query
            #LUKASOVO VERZE
            # query ="INSERT INTO public.expectation_sibling_info(expectation_id, sibling_info_id)VALUES("+str(expectation_id)+","+ str(sibling_info_id) + ");"
            #DANOVA VERZE
            query ="""INSERT INTO public.expectation_sibling_info(expectation_id, sibling_info_id)VALUES(%s, %s);"""
    
        # spusteni query
        cursor.execute(query, (expectation_id, sibling_info_id))

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