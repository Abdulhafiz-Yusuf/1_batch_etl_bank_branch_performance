{{ config(
    materialized = 'incremental',
    unique_key = ['branch_id', 'performance_date']
) }}

WITH silver AS (

    SELECT *
    FROM {{ ref('int_clean_branch_performance') }}

    {% if is_incremental() %}
        WHERE performance_date >= (
            SELECT MAX(performance_date) FROM {{ this }}
        )
    {% endif %}

),

final AS (

    SELECT
        -- Grain
        branch_id,
        performance_date,

        -- Descriptive attribute
        branch_name,

        -- Financial facts
        total_deposits,
        total_loans,
        net_profit,
        operating_expenses,

        -- Operational facts
        new_accounts,
        closed_accounts,

        -- Derived KPI (Gold logic allowed)
        (total_deposits - total_loans) AS liquidity_gap

    FROM silver

)

SELECT *
FROM final
