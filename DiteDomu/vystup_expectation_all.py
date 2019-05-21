import psycopg2
import psycopg2.extras

try:
    # nastaceni databazoveho spojeni
    connection = psycopg2.connect(user="xdejergsdhhzyv", password="0fafa17768bacb33d48bd827065760dc7b9999ca0d1dd33aa75e1c13d47562ab",
                                  host="ec2-79-125-4-72.eu-west-1.compute.amazonaws.com", port="5432", database="d18ffe46fqbrdj")

    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # vypise vsechny verejne udaje z tabulky family,
    query = """SELECT 
	e.family_id,
	sex.name 			AS pref_pohlavi,
	ag.name 			AS pref_vek,
	an.name 			AS pref_anamneza,
	et.name 			AS pref_ethnicity,
	ls.name 			AS pref_pravni_stav,
	mh.name 			AS pref_mental_postizeni,
	ph.name 			as pref_fyz_postizeni
FROM public.expectation as e

join public.sex on sex.Id = e.sex_id

LEFT JOIN public.expectation_age AS ea 	ON ea.expectation_id 	= e.id 
LEFT JOIN public.age AS ag 				ON ea.age_id 			= ag.id

LEFT JOIN public.expectation_anamnesis AS ean ON e.id = ean.expectation_id 
LEFT JOIN public.anamnesis AS an ON ean.anamnesis_id = an.id

LEFT JOIN public.expectation_ethnicity AS eet ON e.id = eet.expectation_id 
LEFT JOIN public.ethnicity AS et ON eet.ethnicity_id = et.id

LEFT JOIN public.expectation_legal_status AS els ON e.id = els.expectation_id 
LEFT JOIN public.legal_status AS ls ON els.legal_status_id = ls.id

LEFT JOIN public.expectation_mental_handicap AS emh ON e.id = emh.expectation_id 
LEFT JOIN public.mental_handicap AS mh ON emh.mental_handicap_id = mh.id

LEFT JOIN public.expectation_physical_handicap AS eph ON e.id = eph.expectation_id 
LEFT JOIN public.physical_handicap AS ph ON eph.physical_handicap_id = ph.id

ORDER BY family_id;"""
    # WHERE xxx AND id_zavod=%s znamena ze vyberea data pro nejaky zavod, ktery zvolil uzivatel
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
