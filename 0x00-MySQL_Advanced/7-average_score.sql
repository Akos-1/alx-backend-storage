-- SQL script to create a stored procedure ComputeAverageScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_score DECIMAL(10,2);
    DECLARE total_count INT;

    -- Compute total score and count of corrections
    SELECT SUM(score), COUNT(*) INTO total_score, total_count
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate average score
    IF total_count > 0 THEN
        UPDATE users
        SET average_score = total_score / total_count
        WHERE id = user_id;
    ELSE
        -- Set average score to 0 if no corrections found
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;

END//

DELIMITER ;
