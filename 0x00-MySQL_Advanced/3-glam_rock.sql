-- SQL script to list all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, 
       TIMESTAMPDIFF(YEAR, formed, IFNULL(split, '2022')) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
