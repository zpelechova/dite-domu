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
    
    cursor.execute("truncate expectation_sibling_info cascade")
    cursor.execute("ALTER SEQUENCE expectation_sibling_info_id_seq RESTART")
    
    for i in range(1, 20):
        #definice sloupcu
        expectation_id = random.randint(1,19)
        #VYGENERUJE JEN JEDNU MOZNOST, NUTNO OTESTOVAT MULTICHOICE
        sibling_info_id = random.randint(1,4)
             

    # definice query
        query = "INSERT INTO public.expectation_sibling_info(expectation_id, sibling_info_id)VALUES("+str(expectation_id)+","+ str(sibling_info_id) + ");"
        # spusteni query
        cursor.execute(query)

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