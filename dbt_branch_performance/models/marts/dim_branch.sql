{{ config(
    materialized = 'table'
) }}

with base as (

    select
        branch_id,
        branch_name

    from {{ ref('stg_bank_branch_performance') }}

)

select
    branch_id,
    branch_name,

    -- metadata (optional but professional)
    current_timestamp as record_loaded_at

from base
group by
    branch_id,
    branch_name
order by branch_id