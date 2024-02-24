-- SQL script to create a function SafeDiv
DELIMITER //

CREATE FUNCTION SafeDiv (numerator DECIMAL(10,2), denominator DECIMAL(10,2))
RETURNS DECIMAL(10,2)
BEGIN
    DECLARE result DECIMAL(10,2);
    
    IF denominator = 0 THEN
        SET result = 0;
    ELSE
        SET result = numerator / denominator;
    END IF;
    
    RETURN result;
END//

DELIMITER ;
