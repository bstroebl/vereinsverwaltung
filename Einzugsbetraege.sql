--select sum(beitrag)::float from (
select vorname, mitgliedsname, CASE eintrittsdatum > '2013-06-01'::date WHEN true then 
COALESCE(individueller_beitrag,12) / 2::float ELSE COALESCE(individueller_beitrag,12) END as beitrag, eintrittsdatum 
from mitglied m
where beitragsgruppe_id = 1 
and eintrittsdatum <= date('2013-12-31'::date 
and zahlungsart_id = 2
order by mitgliedsname, vorname 
--) foo

--SQLLite
-- Beitrag 2015
select vorname, mitgliedsname, 
CASE WHEN eintrittsdatum > date('2015-06-30') THEN
COALESCE(individueller_beitrag,12) / 2 
ELSE COALESCE(individueller_beitrag,12) END as beitrag, 
einzugsermaechtigungsdatum,
eintrittsdatum
from mitglied m
where beitragsgruppe_id = 1 
and eintrittsdatum < date('2016-01-01')
and (austrittsdatum IS NULL or austrittsdatum between date('2015-01-01') and date('2015-12-31'))
and zahlungsart_id = 2
order by mitgliedsname, vorname 
