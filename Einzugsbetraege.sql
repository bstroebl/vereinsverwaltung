--select sum(beitrag)::float from (
select vorname, mitgliedsname, CASE eintrittsdatum > '2013-06-01'::date WHEN true then 
COALESCE(individueller_beitrag,12) / 2::float ELSE COALESCE(individueller_beitrag,12) END as beitrag, eintrittsdatum 
from mitglied m
where beitragsgruppe_id = 1 
and eintrittsdatum <= '2013-12-31'::date 
and zahlungsart_id = 2
order by mitgliedsname, vorname 
--) foo