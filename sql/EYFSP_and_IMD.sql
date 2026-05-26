select
    eyfsp.lad_code,
    eyfsp.lad_name,
    eyfsp.children_count,
    eyfsp.gld_children_count,
    eyfsp.gld_children_percent,
    imd.avg_score as imd_score
from eyfsp
inner join imd on eyfsp.lad_code = imd.la_code
where
    eyfsp.time_period = '202425' and
    eyfsp.geographic_level = 'Local authority district' and
    eyfsp.country_code = 'E92000001' and
    eyfsp.breakdown_topic = 'Total' and
    eyfsp.breakdown = 'Total' and
    eyfsp.sex = 'Total';