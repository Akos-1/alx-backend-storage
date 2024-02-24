-- Create a temporary table to import the data
CREATE TEMPORARY TABLE IF NOT EXISTS temp_metal_bands AS
SELECT *
FROM metal_bands;

-- Query to rank country origins of bands by the number of non-unique fans
SELECT origin, COUNT(*) AS nb_fans
FROM temp_metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

-- Drop the temporary table after use
DROP TEMPORARY TABLE IF EXISTS temp_metal_bands;
