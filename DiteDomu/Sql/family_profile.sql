
SELECT 
	e.family_id,
	string_agg(distinct sex.name, ', ') 	AS pref_pohlavi,
	string_agg(distinct ag.name, ', ') 		AS pref_vek,
	string_agg(distinct an.name, ', ') 		AS pref_anamneza,
	string_agg(distinct et.name, ', ') 		AS pref_ethnicity,
	string_agg(distinct ls.name, ', ') 		AS pref_pravni_stav,
	string_agg(distinct mh.name, ', ') 		AS pref_mental_postizeni,
	string_agg(distinct ph.name, ', ') 		as pref_fyz_postizeni,
	
--polozky z family vystupu
  string_agg(distinct rg.name, ', ') AS region,
  string_agg(distinct ds.name, ', ') AS district,
  string_agg(distinct es.name, ', ') AS expectation_status,
  string_agg(distinct ap.name, ', ') AS approval_type,
  string_agg(distinct ca.name, ', ') AS carer_info,
  string_agg(distinct f.prepcourse, ', ')
FROM public.expectation as e

LEFT JOIN public.sex on sex.Id = e.sex_id

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

LEFT JOIN public.family AS f ON f.id = e.family_id
--polozky z family vystupu
LEFT JOIN public.region rg ON f.region_id = rg.id
LEFT JOIN public.district ds ON f.district_id = ds.id
LEFT JOIN public.expectation_status es ON f.expectation_status_id = es.id
LEFT JOIN public.approval_type ap ON f.approval_type_id = ap.id
LEFT JOIN public.carer_info ca ON f.carer_info_id = ca.id


--priklad filtru na rodinu 1
--where e.family_id = 1
-- priklad filtru na vek
--and (variable_vek is null or (variable_vek is not null and age = variable_vek))
GROUP BY e.family_id
ORDER BY e.family_id
;






















--view_family_profile

with family as
(SELECT f.id,
    rg.name AS region,
    ds.name AS district,
    es.name AS expectation_status,
    ap.name AS approval_type,
    ca.name AS carer_info,
    f.prepcourse
   FROM family f
     LEFT JOIN region rg ON f.region_id = rg.id
     LEFT JOIN district ds ON f.district_id = ds.id
     LEFT JOIN expectation_status es ON f.expectation_status_id = es.id
     LEFT JOIN approval_type ap ON f.approval_type_id = ap.id
     LEFT JOIN carer_info ca ON f.carer_info_id = ca.id
  ORDER BY f.id DESC
)
and
view_expectation as
(SELECT e.family_id,
    ag.name AS pref_vek,
    s.name AS pref_pohlavi,
    sb.name AS pref_sourozenci,
    ph.name AS pref_fyz_postizeni,
    mh.name AS pref_mental_postizeni,
    et.name AS pref_ethnicity,
    an.name AS pref_anamneza,
    ls.name AS pref_pravni_stav
   FROM expectation e
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
  ORDER BY e.family_id)
SELECT
f.id,
rg.name AS region,
ds.name AS district,
es.name AS expectation_status,
ap.name AS approval_type,
ca.name AS carer_info,
f.prepcourse,
e.family_id,
ag.name AS pref_vek,
s.name AS pref_pohlavi,
sb.name AS pref_sourozenci,
ph.name AS pref_fyz_postizeni,
mh.name AS pref_mental_postizeni,
et.name AS pref_ethnicity,
an.name AS pref_anamneza,
ls.name AS pref_pravni_stav
;