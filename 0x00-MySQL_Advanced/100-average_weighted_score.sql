-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_weighted_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    
    -- Calculate total weighted score and total weight
    SELECT SUM(score * weight), SUM(weight)
    INTO total_weighted_score, total_weight
    FROM corrections
    WHERE student_id = user_id;
    
    -- Calculate average weighted score
    IF total_weight > 0 THEN
        UPDATE students
        SET average_weighted_score = total_weighted_score / total_weight
        WHERE id = user_id;
    ELSE
        -- Set average weighted score to 0 if no corrections found
        UPDATE students
        SET average_weighted_score = 0
        WHERE id = user_id;
    END IF;
    
END//

DELIMITER ;
