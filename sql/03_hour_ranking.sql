SELECT
    DATE(ts)               AS day,
    strftime('%H', ts)    AS hour,
    price,
    ROW_NUMBER() OVER (PARTITION BY DATE(ts) ORDER BY price ASC)  AS cheapest_rank,
    ROW_NUMBER() OVER (PARTITION BY DATE(ts) ORDER BY price DESC) AS dearest_rank
FROM prices
WHERE DATE(ts) = '2025-01-15'
ORDER BY cheapest_rank;