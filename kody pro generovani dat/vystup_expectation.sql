SELECT family_id,
ag.name AS expectation_age,
s.name AS expectation_sex,
sb.name AS expectation_sibling_info,
ph.name AS expectation_physical_handicap,
mh.name AS expectation_mental_handicap,
et.name AS expectation_ethnicity,
an.name AS expectation_anamnesis,
ls.name AS expectation_legal_status
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
LEFT JOIN public.expectation_sibling_info AS esb ON e.id = esb.expectation_id 
LEFT JOIN public.sibling_info AS sb ON esb.sibling_info_id = sb.id
LEFT JOIN public.sex AS s ON e.sex_id = s.id
ORDER BY family_id