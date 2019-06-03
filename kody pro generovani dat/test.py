import random
import datetime


# created_on = datetime.datetime.now()
# print(created_on)
import random
import time
# def getRandomDate(startDate, endDate ):
#     print("Printing random date between", startDate, " and ", endDate)
#     randomGenerator = random.random()
#     dateFormat = '%Y-%m-%d'
#     startTime = time.mktime(time.strptime(startDate, dateFormat))
#     endTime = time.mktime(time.strptime(endDate, dateFormat))
#     randomTime = startTime + randomGenerator * (endTime - startTime)
#     randomDate = time.strftime(dateFormat, time.localtime(randomTime))
#     return randomDate
# print ("Random Date = ", getRandomDate("2016-1-1", "2019-1-1"))

#vypise vsechny verejne udaje z tabulky family,approval_type,family_parent, child_in_care
    # query="""SELECT file_number, at.name AS approval_type, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id
    #         FROM public.family as f
    #         LEFT JOIN public.approval_type AS at ON f.approval_type_id = at.id
    #         LEFT JOIN public.family_parent AS fp ON f.
    #         ORDER BY region_id;"""

districty=range(1,78)
print(districty)

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
# CP
##Pozor nedriv query na vyber family_id kde carer_infoid = 2 tzn. 2 rodice

    select_families = """SELECT id from public.family WHERE carer_info_id=1;"""
    cursor.execute(select_families)
    res = cursor.fetchall()
    print(res)
    for i in res:
        print(i)
        # definice sloupcu
        family_id = i[0]
        #pohlavi omezeno na moznosti 1 a 2
        sex_id = random.randint(1,2)
        year_of_birth = random.randint((1965,1990)
        # definice query            
        query ="""INSERT INTO public.family_parent(family_id, sex_id, year_of_birth)VALUES(%s, %s, %s);"""
    
        # spusteni query
        cursor.execute(query, (family_id, sex_id, year_of_birth))
        

    select_families = """SELECT id from public.family WHERE carer_info_id=2;"""
    cursor.execute(select_families)
    result = cursor.fetchall()
    print(result)
    for i in result:
        print(i)
        # definice sloupcu
        family_id = i[0]
        
        #pohlavi omezeno na moznosti 1 a 2
        #generuje pocet rodicu 1-2, vytvori seznam hodnot
        num_sexs = 2
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
        query ="""INSERT INTO public.family_parent(family_id, sex_id, year_of_birth)VALUES(%s, %s, %s);"""
    
        # spusteni query
        cursor.execute(query, (family_id, sex_id, year_of_birth))

    connection.commit()


# CP
    for i in range(1, 201):
        # definice sloupcu
        
        family_id = i
        #pohlavi omezeno na moznosti 1 a 2
        #generuje pocet rodicu 1-2, vytvori seznam hodnot
        num_sexs = carer_info_id
        sex_ids = []
        num_year_of_births = num_sexs
        year_of_birth_list = []
        
        while len(sex_ids) < num_sexs:
            sex_id = random.randint(1,2)
            sex_ids.append(sex_id)
            # roky/years k 'year_of_birth' pro rodice
            year_of_birth = random.randint(1965,1990)
            year_of_birth_list.append(year_of_birth)
        
        for sex_id in sex_ids:
            # definice query
            
            query ="""INSERT INTO public.family_parent(family_id, sex_id, year_of_birth)VALUES(%s, %s, %s);"""
    
            # spusteni query
            cursor.execute(query, (family_id, sex_id, year_of_birth))
          

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
