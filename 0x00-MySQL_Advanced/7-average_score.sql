-- SQL script to create a stored procedure ComputeAverageScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN student_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(5,2);

    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE student_id = student_id;

    UPDATE students
    SET average_score = avg_score
    WHERE id = student_id;
END//

DELIMITER ;
