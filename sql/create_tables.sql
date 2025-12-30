
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.bank_branch_performance (
    branch_id VARCHAR(20) NOT NULL,
    branch_name VARCHAR(100),
    performance_date DATE NOT NULL,
    
    -- metrics
    total_deposits DECIMAL(18, 2),
    total_loans DECIMAL(18, 2),
    new_accounts INT,
    closed_accounts INT,
    net_profit DECIMAL(18, 2),
    operating_expenses DECIMAL(18, 2),

    -- primary key for idempotency + business grain
    CONSTRAINT pk_branch_performance
        PRIMARY KEY (branch_id, performance_date)
);




-- SELECT
--   COUNT(*) AS total_rows,
--   COUNT(CASE WHEN total_loans::text = 'NaN' THEN 1 END) AS nan_count,
--   COUNT(CASE WHEN total_loans IS NULL THEN 1 END) AS null_count
-- FROM silver.int_clean_branch_performance;




