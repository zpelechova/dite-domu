import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # test spojeni, vypise obsah sloupce ID z tabulky
    # query = "select * from approval_type"
    # cursor.execute(query)
    # result = cursor.fetchall()
    #for row in result:
    #    print("Id = ", row[0])

    # vyprazdneni tabulky
    #????myslim neni nutne, vyprazdneni tabulek je u account tab
    cursor.execute("truncate child_in_care cascade")
    cursor.execute("ALTER SEQUENCE child_in_care_id_seq RESTART")
    for i in range(1, 20):
        # definice sloupcu
        family_id = random.randint(1,19)
        #pohlavi omezeno na moznosti 1 a 2
        sex_id = random.randint(1,2)
        relationship_id = random.randint(1,3)
        # roky/years k 'year_of_birth' pro deti v peci rodiny
        years = list(range(2001,2019))
        date_of_birth = random.choice(years)
       

        # definice query
        query = "INSERT INTO public.child_in_care(family_id, sex_id, relationship_id, year_of_birth)VALUES("+str(family_id)+","+ str(sex_id) + "," + str(relationship_id) + "," + str(date_of_birth)+");"
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