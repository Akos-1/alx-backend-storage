-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE user_cursor CURSOR FOR
        SELECT id
        FROM users;
    
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    
    -- Declare variables for calculation
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE avg_weighted_score DECIMAL(10, 2);
    
    -- Declare continue handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Open the cursor
    OPEN user_cursor;
    
    -- Loop through each user
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        -- Calculate total score and total weight for the user
        SELECT SUM(score * weight), SUM(weight)
        INTO total_score, total_weight
        FROM corrections
        WHERE student_id = user_id;
        
        -- Calculate average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;
        
        -- Update average weighted score for the user
        UPDATE users
        SET average_weighted_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP user_loop;
    
    -- Close the cursor
    CLOSE user_cursor;
    
END//

DELIMITER ;
