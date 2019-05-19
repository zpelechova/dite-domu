#draft
query = """SELECT family_id, e.id AS expectation_id_original,
ea.expectation_id AS expectation_id_ea, 
sex_id AS pref_pohlavi,
ea.age_id, 
ag.name AS pref_vek,
an.name AS pref_anamneza,
et.name AS pref_ethnicity,
ls.name AS pref_pravni_stav,
mh.name AS pref_mental_postizeni,
ph.name pref_fyz_postizeni
FROM public.expectation as e
LEFT JOIN public.expectation_age AS ea ON e.id = ea.expectation_id 
LEFT JOIN public.age AS ag ON ea.age_id = ag.id
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