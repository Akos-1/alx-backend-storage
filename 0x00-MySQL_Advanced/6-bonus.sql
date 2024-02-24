-- SQL script to create a stored procedure AddBonus
DELIMITER //

CREATE PROCEDURE AddBonus (
    IN student_id INT,
    IN course_id INT,
    IN bonus_score DECIMAL(5,2)
)
BEGIN
    INSERT INTO corrections (student_id, course_id, score)
    VALUES (student_id, course_id, bonus_score);
END//

DELIMITER ;
