-- SQL script to create a trigger that resets the attribute valid_email only when the email has been changed
CREATE TRIGGER reset_valid_email_on_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0; -- Assuming 0 means invalid email
    END IF;
END;
