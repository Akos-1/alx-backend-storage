-- Import the data from the SQL dump file
SOURCE '/path/to/Downloads/metal_bands.sql';

-- Query to rank country origins of bands by the number of non-unique fans
SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
