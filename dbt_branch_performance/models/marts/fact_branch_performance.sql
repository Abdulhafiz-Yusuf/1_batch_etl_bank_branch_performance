-- models/marts/mart_bank_branch_performance.sql
with base as (

    select *
    from {{ ref('int_branch_monthly') }}

),

kpis as (

    select
        branch_id,
        branch_name,
        month,
        total_deposits,
        total_loans,
        new_accounts,
        closed_accounts,
        net_profit,
        operating_expenses,

        -- Derived KPIs
        case when total_deposits = 0 then null
             else total_loans::numeric / total_deposits::numeric
        end as loan_to_deposit_ratio,

        case when new_accounts = 0 then null
             else net_profit::numeric / new_accounts::numeric
        end as profit_per_new_account

    from base

)

select *
from kpis
