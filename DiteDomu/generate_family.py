import psycopg2
import random


try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user = "xdejergsdhhzyv",password = "0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",host = "ec2-79-125-4-72.eu-west-1.compute.amazonaws.com",port = "5432",database = "d18ffe46fqbrdj")
    
    cursor = connection.cursor()

    # vyprazdneni tabulky
    #????myslim neni nutne, vyprazdneni tabulek je u account tab
    # cursor.execute("truncate child_in_care cascade")
    # cursor.execute("ALTER SEQUENCE child_in_care_id_seq RESTART")
    # cursor.execute("truncate family_parent cascade")
    # cursor.execute("ALTER SEQUENCE family_parent_id_seq RESTART")
    cursor.execute("truncate family cascade")
    cursor.execute("ALTER SEQUENCE family_id_seq RESTART")

    for i in range(1, 20):
        # definice sloupcu
        account_id = i
        file_number = "file_number_test"
        approval_type_id = random.randint(1,2)
        regional_office_id = 11 # stredocesky kraj
        expectation_status_id = random.randint(1,2)
        region_id = 11 # stredocesky kraj


        # districty k stredoceskemu kraji
        districts = [1, 2, 27, 29, 31, 35, 36, 40, 51, 52, 56, 57]
        district_id = random.choice(districts)
                
        carer_info_id = random.randint(1,2)
        prepcourse = "prepcourse_test"
        
        #nove sloupce
        note = "notes_test"
        # datumy nahodne pro approval_date
        dates = ['2017-3-23', '2019-2-1', '2017-10-12', '2018-2-3']
        approval_date = random.choice(dates)
        
        
        # definice query
        query = "INSERT INTO public.family(file_number, approval_type_id, regional_office_id,expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id, note, approval_date) VALUES ('" + file_number +"',"+ str(approval_type_id) + "," + str(regional_office_id) + "," + str(expectation_status_id) + "," + str(region_id) + "," + str(district_id) +"," + str(carer_info_id) + ",'" + prepcourse +"'," + str(account_id) + ",'" + note +"','" + approval_date +"');"
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