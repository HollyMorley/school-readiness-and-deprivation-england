select
    eyfsp.lad_code
    ,eyfsp.lad_name
    ,eyfsp.new_la_code
    ,eyfsp.la_name
    ,eyfsp.gld_children_percent
    ,imd.avg_score as imd_score
    ,takeup.percentage_eligible_children as eyp_takeup
    ,ofsted.weighted_score as ofsted_weighted_score
    ,sen_total.percentage_children as sen_prevalence
    ,(sen_ehc.percentage_children / sen_total.percentage_children) * 100 as sen_ehc_rate
    ,(sen_nursery.number_children / (sen_nursery.number_children + sen_reception.number_children)) * 100 as sen_early_identification_rate

from eyfsp eyfsp

inner join imd  imd on eyfsp.lad_code = imd.la_code

inner join takeup takeup on eyfsp.new_la_code = takeup.new_la_code
    and takeup.entitlement_type = 'Universal'
    and takeup.age = 'Total'
    and takeup.time_period = 2025
    and takeup.geographic_level = 'Local authority'

inner join (
    select
        new_la_code,
        sum(case
            when ofsted_judgement = 'Outstanding' then 4 * percentage_children
            when ofsted_judgement = 'Good' then 3 * percentage_children
            when ofsted_judgement = 'Requires improvement' then 2 * percentage_children
            when ofsted_judgement = 'Inadequate' then 1 * percentage_children
        end) / 100.0 as weighted_score
    from ofsted
    where entitlement_type = 'Universal'
        and age = 'Total'
        and time_period = 2025
        and geographic_level = 'Local authority'
        and ofsted_judgement != 'Total'
    group by new_la_code
) ofsted on eyfsp.new_la_code = ofsted.new_la_code

inner join (
    select
        new_la_code,
        percentage_children
    from sen
    where entitlement_type = 'Universal'
        and year_group = 'Total'
        and age = 'Total'
        and ethnicity_major = 'Total'
        and time_period = 2025
        and geographic_level = 'Local authority'
        and sen = 'SEN'
        and sen_provision = 'Total'
    group by new_la_code
) sen_total on eyfsp.new_la_code = sen_total.new_la_code

inner join (
    select
        new_la_code,
        percentage_children
    from sen
    where entitlement_type = 'Universal'
        and year_group = 'Total'
        and age = 'Total'
        and ethnicity_major = 'Total'
        and time_period = 2025
        and geographic_level = 'Local authority'
        and sen = 'SEN'
        and sen_provision = 'EHC plan'
    group by new_la_code
) sen_ehc on eyfsp.new_la_code = sen_ehc.new_la_code

inner join (
    select
        new_la_code,
        number_children
    from sen
    where entitlement_type = 'Universal'
        and year_group = 'Nursery'
        and age = 'Total'
        and ethnicity_major = 'Total'
        and time_period = 2025
        and geographic_level = 'Local authority'
        and sen = 'SEN'
        and sen_provision = 'Total'
) sen_nursery on eyfsp.new_la_code = sen_nursery.new_la_code

inner join (
    select
        new_la_code,
        number_children
    from sen
    where entitlement_type = 'Universal'
        and year_group = 'Reception'
        and age = 'Total'
        and ethnicity_major = 'Total'
        and time_period = 2025
        and geographic_level = 'Local authority'
        and sen = 'SEN'
        and sen_provision = 'Total'
) sen_reception on eyfsp.new_la_code = sen_reception.new_la_code

where
    eyfsp.time_period = '202425'
    and eyfsp.geographic_level = 'Local authority district'
    and eyfsp.country_code = 'E92000001'
    and eyfsp.breakdown_topic = 'Total'
    and eyfsp.breakdown = 'Total'
    and eyfsp.sex = 'Total'

    ;