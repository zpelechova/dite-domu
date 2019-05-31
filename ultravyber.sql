SELECT f.id AS family_id,
file_number,
approval_date,
prepcourse,
note,
number_child_in_care,
ap.name AS approval_type,
ro.name AS regional_office,
es.name AS expectation_status,
ds.name AS district,
s2.name_child as youngest_child_sex, 
rl.name AS youngest_child_relationship, 
cc.year_of_birth AS youngest_child_year_of_birth,
ci.name AS carer_info,
string_agg(DISTINCT s3.name_adult, ',') AS parent_sex, 
string_agg(DISTINCT fp.year_of_birth::text, ',') AS parent_year_of_birth,
string_agg(distinct ag.name, ', ') AS expectation_age,
string_agg(distinct s.name_child , ', ') AS expectation_sex,
string_agg(distinct sb.name , ', ') AS expectation_sibling_info,
string_agg(distinct ph.name , ', ') AS expectation_physical_handicap,
string_agg(distinct mh.name , ', ') AS expectation_mental_handicap,
string_agg(distinct et.name , ', ') AS expectation_ethnicity,
string_agg(distinct an.name , ', ') AS expectation_anamnesis,
string_agg(distinct ls.name , ', ') AS expectation_legal_status
FROM family as f
LEFT JOIN public.expectation AS e ON f.id = e.family_id
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
LEFT JOIN public.approval_type AS ap ON f.approval_type_id = ap.id
LEFT JOIN public.regional_office AS ro ON f.regional_office_id = ro.id
LEFT JOIN public.expectation_status AS es ON f.expectation_status_id = es.id
LEFT JOIN public.district AS ds ON f.district_id = ds.id
LEFT JOIN public.child_in_care AS cc ON cc.family_id = f.id
LEFT JOIN public.relationship AS rl ON cc.relationship_id = rl.id
LEFT JOIN public.sex AS s2 ON cc.sex_id = s2.id
LEFT JOIN public.carer_info AS ci ON f.carer_info_id = ci.id
LEFT JOIN public.family_parent AS fp ON fp.family_id = f.id
LEFT JOIN public.sex AS s3 ON fp.sex_id = s3.id
WHERE f.id = %s
GROUP BY f.id, file_number, approval_date, prepcourse, note, number_child_in_care, ap.name, ro.name, es.name, ds.name, s2.name_child, rl.name, cc.year_of_birth, ci.name