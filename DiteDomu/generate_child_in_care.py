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
    cursor.execute("truncate child_in_care cascade")
    cursor.execute("ALTER SEQUENCE child_in_care_id_seq RESTART")

##Pozor nedriv query na vyber family_id kde number of children in care  neni nula nebo null
 select id from public.family where id is not null and id>0
 
    for i in range(1, 501):
        # definice sloupcu
        family_id = i
        #pohlavi omezeno na moznosti 1 a 2
        
        #generuje pocet deti v peci od poctu 0-1, vytvori seznam hodnot
        #zmeneno z poctu 0-4, zaznamenavat bude rodina pouze udaje o nejmladsim diteti
        ##POZOR
        num_sexs = random.randint(0, 1)
        sex_ids = []
        num_relats = num_sexs
        relat_ids = []
        num_year_of_births = num_sexs
        year_of_birth_list = []
        #JE WHILE DOBRE?
        while len(sex_ids) < num_sexs:
            sex_id = random.randint(1,2)
            sex_ids.append(sex_id)
            relat_id = random.randint(1,3)
            relat_ids.append(relat_id)
        # roky/years k 'year_of_birth' pro deti v peci rodiny
            year_of_birth = random.randint(2001,2019)
            year_of_birth_list.append(year_of_birth)
        
        for sex_id in sex_ids:
            # definice query
            #DANOVA VERZE
            query ="""INSERT INTO public.child_in_care(family_id, sex_id, relationship_id, year_of_birth)VALUES(%s, %s, %s,%s,) AS cic
            LEFT JOIN public.family AS f ON f.id = cic.family_id
            WHERE number_child_in_care>1;"""
    
        # spusteni query
        cursor.execute(query, (family_id, sex_id, relationship_id, year_of_birth))
        

    connection.commit()
#CO ZNAMENA CERVENA SIPKA VLEVO?
# v pripade databazove chyby, vyhodit chybu
except (Exception, psycopg2.Error) as error :
    print ("PostgreSQL Exception", error)
# uzavreni databazoveho pripojeni
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")