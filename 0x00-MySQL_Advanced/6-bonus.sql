-- SQL script to create a stored procedure AddBonus
DELIMITER //

CREATE PROCEDURE AddBonus (
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score DECIMAL(5,2)
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- If project doesn't exist, insert it into the projects table
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the correction for the user
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
    
END//

DELIMITER ;
