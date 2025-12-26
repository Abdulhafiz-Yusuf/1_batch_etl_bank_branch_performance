-- models/intermediate/int_bank_branch_performance.sql
with base as (

    select *
    from {{ ref('int_clean_branch_performance') }}
   

),

metrics as (

    select
        branch_id,
        branch_name,
        performance_date,
        sum(total_deposits)       as total_deposits,
        sum(total_loans)          as total_loans,
        sum(new_accounts)         as new_accounts,
        sum(closed_accounts)      as closed_accounts,
        sum(net_profit)           as net_profit,
        sum(operating_expenses)   as operating_expenses
    from base
    group by branch_id, 
            branch_name, 
            performance_date
            

)

select *
from metrics
order by branch_id