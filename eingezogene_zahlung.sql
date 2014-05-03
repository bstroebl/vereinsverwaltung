INSERT INTO zahlung(mitglied_id,betrag,zahldatum,hinweis_id)
select m.id as mitglied_id, CASE eintrittsdatum > '2013-06-01'::date WHEN true then 
COALESCE(individueller_beitrag,12) / 2::float ELSE COALESCE(individueller_beitrag,12) END as betrag, 
'2013-12-13'::date as zahldatum, 2 as hinweis_id
from mitglied m
where beitragsgruppe_id = 1 
and eintrittsdatum <= '2013-12-31'::date 
and zahlungsart_id = 2
and id != 32 --Martin Gräf		