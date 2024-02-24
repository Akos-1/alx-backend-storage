-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    DECLARE average_weighted_score DECIMAL(10,2);

    -- Calculate total score and total weight
    SELECT SUM(score), SUM(weight)
    INTO total_score, total_weight
    FROM corrections
    WHERE student_id = user_id;

    -- Calculate average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = total_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    -- Update the average weighted score for the student
    UPDATE students
    SET average_weighted_score = average_weighted_score
    WHERE id = user_id;

END//

DELIMITER ;

