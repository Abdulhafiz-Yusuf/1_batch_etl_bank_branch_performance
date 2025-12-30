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

        -- Financials with NaN handling
        COALESCE(NULLIF(total_deposits::numeric, 'NaN')::numeric, 0) AS total_deposits,
        COALESCE(NULLIF(total_loans::numeric, 'NaN')::numeric, 0) AS total_loans,
        COALESCE(NULLIF(net_profit::numeric, 'NaN')::numeric, 0) AS net_profit,
        COALESCE(NULLIF(operating_expenses::numeric, 'NaN')::numeric, 0) AS operating_expenses,

        -- Operational metrics with NaN handling
        COALESCE(NULLIF(new_accounts::numeric, 'NaN')::numeric, 0) AS new_accounts,
        COALESCE(NULLIF(closed_accounts::numeric, 'NaN')::numeric, 0) AS closed_accounts

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

        -- Financial sanity (after NaN cleaning)
        AND total_deposits = total_deposits
        AND total_loans = total_loans

        -- Accounts sanity
        AND new_accounts = new_accounts
        AND closed_accounts = closed_accounts

)

SELECT *
FROM sanity_checked