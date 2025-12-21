{{ config(materialized='table') }}

with date_spine as (

    -- Generate a calendar range
    select
        generate_series(
            date '2015-01-01',
            date '2035-12-31',
            interval '1 day'
        )::date as date_day

)

select
    date_day                                   as date_id,   -- PK
    date_day                                   as full_date,

    extract(year from date_day)::int           as year,
    extract(quarter from date_day)::int        as quarter,
    extract(month from date_day)::int          as month,
    to_char(date_day, 'Month')                 as month_name,
    to_char(date_day, 'Mon')                   as month_short,
    extract(day from date_day)::int             as day,
    extract(dow from date_day)::int             as day_of_week,
    to_char(date_day, 'Day')                   as day_name,

    case when extract(dow from date_day) in (0,6)
         then true else false end              as is_weekend,

    case when extract(month from date_day) in (1,2,3)
         then 'Q1'
         when extract(month from date_day) in (4,5,6)
         then 'Q2'
         when extract(month from date_day) in (7,8,9)
         then 'Q3'
         else 'Q4'
    end                                        as fiscal_quarter,

    current_timestamp                          as record_loaded_at

from date_spine
