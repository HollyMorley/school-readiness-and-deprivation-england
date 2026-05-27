select
    eyfsp.lad_code
    ,eyfsp.lad_name
    ,eyfsp.children_count
    ,eyfsp.gld_children_count
    ,eyfsp.gld_children_percent
    ,iod_employment.avg_score as employment_score
    ,iod_education.avg_score as education_score
    ,iod_health.avg_score as health_score
    ,iod_crime.avg_score as crime_score
    ,iod_barriers.avg_score as barriers_score
    ,iod_living.avg_score as living_score
    ,iod_idaci.avg_score as idaci_score
from eyfsp
inner join iod_employment on eyfsp.lad_code = iod_employment.la_code
inner join iod_education on eyfsp.lad_code = iod_education.la_code
inner join iod_health on eyfsp.lad_code = iod_health.la_code
inner join iod_crime on eyfsp.lad_code = iod_crime.la_code
inner join iod_barriers on eyfsp.lad_code = iod_barriers.la_code
inner join iod_living on eyfsp.lad_code = iod_living.la_code
inner join iod_idaci on eyfsp.lad_code = iod_idaci.la_code
where
    eyfsp.time_period = '202425' and
    eyfsp.geographic_level = 'Local authority district' and
    eyfsp.country_code = 'E92000001' and
    eyfsp.breakdown_topic = 'Total' and
    eyfsp.breakdown = 'Total' and
    eyfsp.sex = 'Total';