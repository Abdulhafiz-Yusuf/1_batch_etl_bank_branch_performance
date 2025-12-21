-- models/staging/stg_bank_branch_performance.sql
select
    branch_id,
    branch_name,
    case
        when date is null then null
        else cast(date as date)
    end as performance_date,
    total_deposits,
    total_loans,
    new_accounts,
    closed_accounts,
    net_profit,
    operating_expenses
from {{ source('silver', 'bank_branch_performance') }}
