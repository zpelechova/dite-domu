SELECT * , (podminka1 + podminka2 + podminka3 + podminka4 + podminka5 + podminka6 + podminka7 + podminka8 + podminka9 + podminka10) AS result FROM
(SELECT 
    f.id AS family_id,
    ag.name AS expectation_age,
    s.name AS expectation_sex,
    sb.name AS expectation_sibling_info,
    ph.name AS expectation_physical_handicap,
    mh.name AS expectation_mental_handicap,
    et.name AS expectation_ethnicity,
    an.name AS expectation_anamnesis,
    ls.name AS expectation_legal_status,
    rg.name AS region,
    ds.name AS district,
    es.name AS expectation_status,
    ap.name AS approval_type,
    ca.name AS carer_info,
    f.prepcourse,
    CASE WHEN (%(approval_type_id)s IS NULL OR approval_type_id = %(approval_type_id)s)
    THEN 1
    ELSE 0
    END AS podminka1
    , CASE WHEN (%(sex)s IS NULL OR sex_id = %(sex)s OR sex_id = 3) THEN 1 ELSE 0 END AS podminka2
    , CASE WHEN (%(legal_status_id)s IS NULL OR legal_status_id = %(legal_status_id)s) THEN 1 ELSE 0 END AS podminka3
    , CASE WHEN (%(district_id)s IS NULL OR district_id = %(district_id)s OR district_id = 78) THEN 1 ELSE 0 END AS podminka4
    , CASE WHEN (%(age)s IS NULL OR age_id = %(age)s) THEN 1 ELSE 0 END AS podminka5
    , CASE WHEN (%(siblings)s IS NULL OR esb.sibling_info_id = %(siblings)s) THEN 1 ELSE 0 END AS podminka6
    , CASE WHEN (%(physical_handicap)s IS NULL OR physical_handicap_id = %(physical_handicap)s) THEN 1 ELSE 0 END AS podminka7
    , CASE WHEN (%(mental_handicap)s IS NULL OR mental_handicap_id = %(mental_handicap)s) THEN 1 ELSE 0 END AS podminka8
    , CASE WHEN (%(ethnicity)s IS NULL OR ethnicity_id = %(ethnicity)s) THEN 1 ELSE 0 END AS podminka9
    , CASE WHEN (%(anamnesis)s IS NULL OR anamnesis_id = %(anamnesis)s) THEN 1 ELSE 0 END AS podminka10,
    FROM public.family as f
    LEFT JOIN   PUBLIC.expectation as e ON f.id = e.family_id
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
    LEFT JOIN district ds ON f.district_id = ds.id
    LEFT JOIN region rg ON ds.region_id = rg.id
    LEFT JOIN expectation_status es ON f.expectation_status_id = es.id
    LEFT JOIN approval_type ap ON f.approval_type_id = ap.id
    LEFT JOIN carer_info ca ON f.carer_info_id = ca.id) AS a ORDER BY result DESC
