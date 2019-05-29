 SELECT e.family_id,
    string_agg(DISTINCT ag.name, ', '::text) AS expectation_age,
    string_agg(DISTINCT s.name, ', '::text) AS expectation_sex,
    string_agg(DISTINCT sb.name, ', '::text) AS expectation_sibling_info,
    string_agg(DISTINCT ph.name, ', '::text) AS expectation_physical_handicap,
    string_agg(DISTINCT mh.name, ', '::text) AS expectation_mental_handicap,
    string_agg(DISTINCT et.name, ', '::text) AS expectation_ethnicity,
    string_agg(DISTINCT an.name, ', '::text) AS expectation_anamnesis,
    string_agg(DISTINCT ls.name, ', '::text) AS expectation_legal_status,
    rg.name AS region,
    ds.name AS district,
    es.name AS expectation_status,
    ap.name AS approval_type,
    ca.name AS carer_info,
    f.prepcourse
   FROM family f
     LEFT JOIN expectation e ON f.id = e.family_id
     LEFT JOIN expectation_age ea ON e.id = ea.expectation_id
     LEFT JOIN age ag ON ea.age_id = ag.id
     LEFT JOIN expectation_anamnesis ean ON e.id = ean.expectation_id
     LEFT JOIN anamnesis an ON ean.anamnesis_id = an.id
     LEFT JOIN expectation_ethnicity eet ON e.id = eet.expectation_id
     LEFT JOIN ethnicity et ON eet.ethnicity_id = et.id
     LEFT JOIN expectation_legal_status els ON e.id = els.expectation_id
     LEFT JOIN legal_status ls ON els.legal_status_id = ls.id
     LEFT JOIN expectation_mental_handicap emh ON e.id = emh.expectation_id
     LEFT JOIN mental_handicap mh ON emh.mental_handicap_id = mh.id
     LEFT JOIN expectation_physical_handicap eph ON e.id = eph.expectation_id
     LEFT JOIN physical_handicap ph ON eph.physical_handicap_id = ph.id
     LEFT JOIN expectation_sibling_info esb ON e.id = esb.expectation_id
     LEFT JOIN sibling_info sb ON esb.sibling_info_id = sb.id
     LEFT JOIN sex s ON e.sex_id = s.id
     LEFT JOIN region rg ON f.region_id = rg.id
     LEFT JOIN district ds ON f.district_id = ds.id
     LEFT JOIN expectation_status es ON f.expectation_status_id = es.id
     LEFT JOIN approval_type ap ON f.approval_type_id = ap.id
     LEFT JOIN carer_info ca ON f.carer_info_id = ca.id
  GROUP BY e.family_id, rg.name, ds.name, es.name, ap.name, ca.name, f.prepcourse
  ORDER BY e.family_id DESC;