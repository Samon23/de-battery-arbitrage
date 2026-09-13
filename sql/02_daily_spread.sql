WITH daily AS (
    SELECT
        DATE(ts) AS day,
        MIN(price) OVER (PARTITION BY DATE(ts)) AS day_min,
        MAX(price) OVER (PARTITION BY DATE(ts)) AS day_max
    FROM prices
)
SELECT DISTINCT
    day,
    ROUND(day_max - day_min, 2) AS spread
FROM daily
ORDER BY spread DESC
LIMIT 20;