{{ config(
    materialized = 'incremental',
    unique_key = ['branch_id', 'performance_date']
) }}

WITH source AS (

    SELECT
        -- Rename + standardize
        branch_id                         AS branch_id,
        TRIM(branch_name)                 AS branch_name,
        performance_date                  AS performance_date,

        -- Financials
        total_deposits                    AS total_deposits,
        total_loans                       AS total_loans,
        net_profit                        AS net_profit,
        operating_expenses                AS operating_expenses,

        -- Operational metrics
        new_accounts                      AS new_accounts,
        closed_accounts                   AS closed_accounts

    FROM bronze.bank_branch_performance

    {% if is_incremental() %}
        -- Only process new or changed records
        WHERE performance_date >= (
            SELECT MAX(performance_date) FROM {{ this }}
        )
    {% endif %}

),

sanity_checked AS (

    SELECT *
    FROM source
    WHERE
        -- Hard sanity rules
        branch_id IS NOT NULL
        AND performance_date IS NOT NULL

        -- Financial sanity
        AND total_deposits >= 0
        AND total_loans >= 0

        -- Accounts sanity
        AND new_accounts >= 0
        AND closed_accounts >= 0

)

SELECT *
FROM sanity_checked
