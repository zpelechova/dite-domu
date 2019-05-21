-- Vek ke konkretni family
select age.name
from expectation_age
join expectation on expectation.Id = expectation_age.expectation_id
join age on age.Id = expectation_age.age_id
where family_id = 1



-- vypis expectations => agregovane sloupce
SELECT 
	e.family_id,
	string_agg(distinct sex.name, ', ') 	AS pref_pohlavi,
	string_agg(distinct ag.name, ', ') 		AS pref_vek,
	string_agg(distinct an.name, ', ') 		AS pref_anamneza,
	string_agg(distinct et.name, ', ') 		AS pref_ethnicity,
	string_agg(distinct ls.name, ', ') 		AS pref_pravni_stav,
	string_agg(distinct mh.name, ', ') 		AS pref_mental_postizeni,
	string_agg(distinct ph.name, ', ') 		as pref_fyz_postizeni
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
--priklad filtru na rodinu 1
where family_id = 1
-- priklad filtru na vek
--and (variable_vek is null or (variable_vek is not null and age = variable_vek))
group by family_id
ORDER BY family_id;

--rodice ke konkretni rodine
--POZOR NEDA JEN JEDNO POLE - budou 2 pole pro kazdeho rodice, 
--ZUZA do formulare nutno udelat 4 pole pro kazdou rodinu
SELECT 
--fp.family_id, fp.id AS "id_rodic", 
s.name AS "pohlavi_rodic", 
fp.year_of_birth AS "datum_narozeni_rodic"
FROM public.family_parent AS fp
LEFT JOIN public.sex AS s ON fp.sex_id = s.id
WHERE fp.family_id = 1;

-- deti ke konkretni rodine
-- POZOR NEDA JEN JEDNO POLE - budou 3 pole pro kazde stavajici dite v rodine, pocet deti neznamy asi nutno agregovat
--overit na skupinkach s Danem
SELECT 
--cic.family_id, cic.id AS "id_dite", 
sum(count (cic.id))
s.name AS "pohlavi_dite", 
rel.name AS "vztah_k_rodine", 
cic.year_of_birth AS "datum_narozeni_dite"
FROM public.child_in_care as cic
LEFT JOIN public.relationship AS rel ON cic.relationship_id = rel.id
LEFT JOIN public.sex AS s ON cic.sex_id = s.id;