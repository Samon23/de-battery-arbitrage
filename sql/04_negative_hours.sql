WITH tagged AS (
    SELECT
        strftime('%Y-%m', ts) AS month,
        CASE WHEN price < 0 THEN 1 ELSE 0 END AS is_negative
    FROM prices
)
SELECT
    month,
    SUM(is_negative)                                  AS negative_hours,
    COUNT(*)                                          AS total_hours,
    ROUND(100.0 * SUM(is_negative) / COUNT(*), 1)     AS pct_negative
FROM tagged
GROUP BY month
ORDER BY month;