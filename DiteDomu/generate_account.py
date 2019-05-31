import psycopg2
import random
from datetime import date


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
    cursor.execute("truncate account cascade")
    cursor.execute("ALTER SEQUENCE account_id_seq RESTART")

    cursor.execute("truncate family cascade")
    cursor.execute("ALTER SEQUENCE family_id_seq RESTART")

    cursor.execute("truncate child_in_care cascade")
    cursor.execute("ALTER SEQUENCE child_in_care_id_seq RESTART")
    cursor.execute("truncate family_parent cascade")
    cursor.execute("ALTER SEQUENCE family_parent_id_seq RESTART")
    cursor.execute("truncate expectation cascade")
    cursor.execute("ALTER SEQUENCE expectation_id_seq RESTART")

    cursor.execute("truncate expectation_age cascade")
    cursor.execute("ALTER SEQUENCE expectation_age_id_seq RESTART")
    cursor.execute("truncate expectation_anamnesis cascade")
    cursor.execute("ALTER SEQUENCE expectation_anamnesis_id_seq RESTART")
    cursor.execute("truncate expectation_ethnicity cascade")
    cursor.execute("ALTER SEQUENCE expectation_ethnicity_id_seq RESTART")
    cursor.execute("truncate expectation_legal_status cascade")
    cursor.execute("ALTER SEQUENCE expectation_legal_status_id_seq RESTART")
    cursor.execute("truncate expectation_physical_handicap cascade")
    cursor.execute("ALTER SEQUENCE expectation_physical_handicap_id_seq RESTART")
    cursor.execute("truncate expectation_mental_handicap cascade")
    cursor.execute("ALTER SEQUENCE expectation_mental_handicap_id_seq RESTART")
    cursor.execute("truncate expectation_sibling_info cascade")
    cursor.execute("ALTER SEQUENCE expectation_sibling_info_id_seq RESTART")
    
    for i in range(1, 201):
        # definice sloupcu - password, email, telephone, role_id, account_status_id, account_deactivation_reason_id, officer_first_name, officer_last_name, officer_position_name)
        
        password = "password_test"+ str(i)
        email = "jmeno_prijmeni" + str(i) + "@domena.com"
        role_id = 2
        #generuji pouze aktivni ucty rodin
        
        account_status_id = 1
        # account_status omezene na aktivni
        # statuses = [1, 3]
        # account_status_id = random.choice(statuses)
        #account_status_id = nenastaveno, generuji pouze aktivni ucty
        #sloupce platne jen pro KU nevyplnuji
        #telephone = random.randint (111111111,999999999)
        # officer_first_name = "NA"+ str(i)
        # officer_last_name = "NA"+ str(i)
        # officer_position_name = "NA"+ str(i)

        # definice query
        
        query = """INSERT INTO public.account(password, email, role_id, account_status_id )VALUES( %s, %s, %s, %s);"""
        # spusteni query
        cursor.execute(query, (password, email, role_id, account_status_id))

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