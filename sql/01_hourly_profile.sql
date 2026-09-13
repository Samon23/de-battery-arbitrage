SELECT
    CAST(strftime('%H', ts) AS INTEGER) AS hour_of_day,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(MIN(price), 2) AS min_price,
    ROUND(MAX(price), 2) AS max_price,
    COUNT(*)             AS n_hours
FROM prices
GROUP BY hour_of_day
ORDER BY hour_of_day;