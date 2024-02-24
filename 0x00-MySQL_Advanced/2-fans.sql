-- SQL script to rank country origins of bands by the number of (non-unique) fans
SELECT origin, SUM(nb_fans) AS total_fans
FROM (
    SELECT origin, COUNT(*) AS nb_fans
    FROM metal_bands
    GROUP BY origin
) AS subquery
GROUP BY origin
ORDER BY total_fans DESC;
