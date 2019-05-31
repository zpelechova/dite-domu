import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from expectation_age"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    cursor.execute("truncate expectation_age cascade")
    cursor.execute("ALTER SEQUENCE expectation_age_id_seq RESTART")
    for i in range(1,201):
        # definice sloupcu
        family_id = i
        #nagenerovani poctu zvolenych moznosti
        num_ages = random.randint(1, 5)
        age_ids = []
        
        while len(age_ids) < num_ages:
            age_id = random.randint(1, 5)
            if age_id not in age_ids:
                age_ids.append(age_id)
        
        for age_id in age_ids:
            # definice query
            query = """INSERT INTO public.expectation_age(family_id, age_id)VALUES(%s, %s);"""
            # spusteni query
            cursor.execute(query, (family_id, age_id))
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