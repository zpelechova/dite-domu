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
    
    cursor.execute("truncate family_parent cascade")
    cursor.execute("ALTER SEQUENCE family_parent_id_seq RESTART")
    
#Nedriv query na vyber family_id kde carer_infoid = 2 tzn. 2 rodice

    select_families = """SELECT id from public.family WHERE carer_info_id=2;"""
    cursor.execute(select_families)
    res = cursor.fetchall()
    # na zkousku
    #print(res)
    seznam = [x[0] for x in res]
    #print(seznam)
    for i in range(1, 201):
        family_id = i
        if i in seznam:
            num_sexs = 2
        else:
            num_sexs = 1
            
        sex_ids = []
        num_year_of_births = num_sexs
        year_of_birth_list = []
        while len(sex_ids) < num_sexs:
            sex_id = random.randint(1,2)
            sex_ids.append(sex_id)
                # roky/years k 'year_of_birth' pro rodice
            year_of_birth = random.randint(1965,1990)
            year_of_birth_list.append(year_of_birth)
    
            # definice query            
            sql ="""INSERT INTO public.family_parent(family_id, sex_id, year_of_birth)VALUES(%s, %s, %s);"""
    
            # spusteni query
            cursor.execute(sql, (family_id, sex_id, year_of_birth))


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