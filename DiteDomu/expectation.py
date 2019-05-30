import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    
    cursor.execute("truncate expectation cascade")
    cursor.execute("ALTER SEQUENCE expectation_id_seq RESTART")
    for i in range(1, 501):
        # definice sloupcu
        ##NUTNO OPRAVIT ABY BRALO POSLEDNI ID, KOD Zuza?
        family_id = i
        sex_id = random.randint(1,3)
        
       

        # definice query
        query = "INSERT INTO public.expectation(family_id, sex_id)VALUES("+str(family_id)+","+ str(sex_id) + ");"
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