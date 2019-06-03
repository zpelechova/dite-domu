import psycopg2
import psycopg2.extras

try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user="xdejergsdhhzyv", password="0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",
                                  host="ec2-79-125-4-72.eu-west-1.compute.amazonaws.com", port="5432", database="d18ffe46fqbrdj")

    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # vypise vsechny verejne udaje z tabulky family_parent child in care,
    query = """WITH child_in_care_table AS (SELECT cic.family_id, cic.id AS "id_dite", s.name AS "pohlavi_dite", rel.name AS "vztah_k_rodine", 
cic.year_of_birth AS "datum_narozeni_dite" FROM public.child_in_care as cic
LEFT JOIN public.relationship AS rel ON cic.relationship_id = rel.id
LEFT JOIN public.sex AS s ON cic.sex_id = s.id)
, family_parent_table AS
(SELECT fp.family_id, fp.id AS "id_rodic", s.name AS "pohlavi_rodic", 
 fp.year_of_birth AS "datum_narozeni_rodic"
FROM public.family_parent as fp
LEFT JOIN public.sex AS s ON fp.sex_id = s.id)
SELECT * FROM family_parent_table as fp
LEFT JOIN child_in_care_table AS cic ON fp.family_id = cic.family_id;"""

##verze 2 - child and parent zvlast
query="""SELECT fp.family_id, fp.id AS "id_rodic", s.name AS "pohlavi_rodic", 
 fp.year_of_birth AS "datum_narozeni_rodic"
FROM public.family_parent as fp
LEFT JOIN public.sex AS s ON fp.sex_id = s.id;"""
query = """SELECT cic.family_id, cic.id AS "id_dite", s.name AS "pohlavi_dite", rel.name AS "vztah_k_rodine", 
cic.year_of_birth AS "datum_narozeni_dite"
FROM public.child_in_care as cic
LEFT JOIN public.relationship AS rel ON cic.relationship_id = rel.id
LEFT JOIN public.sex AS s ON cic.sex_id = s.id;"""

#verze 3 union all odmazano rel.name AS "vztah_k_rodine",
query = """SELECT fp.family_id, fp.id AS "id_rodic", s.name AS "pohlavi_rodic", 
fp.year_of_birth AS "datum_narozeni_rodic"
FROM public.family_parent as fp
LEFT JOIN public.sex AS s ON fp.sex_id = s.id
UNION ALL
SELECT cic.family_id, cic.id AS "id_dite", s.name AS "pohlavi_dite",
cic.year_of_birth AS "datum_narozeni_dite"
FROM public.child_in_care as cic
LEFT JOIN public.relationship AS rel ON cic.relationship_id = rel.id
LEFT JOIN public.sex AS s ON cic.sex_id = s.id
;"""

    # POZOR NA ODSAZENI
# spusteni query
    cursor.execute(query)
    res = cursor.fetchall()
    print(res)
    # for r in res:
    #     print(r['approval_type'])

# v pripade databazove chyby, vyhodit chybu
except (Exception, psycopg2.Error) as error:
    print("PostgreSQL Exception", error)
# uzavreni databazoveho pripojeni
finally:
    # close communication with the database
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
