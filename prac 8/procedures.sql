
CREATE OR REPLACE PROCEDURE upsert_u(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
        UPDATE phonebook SET phone = p_phone WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone) VALUES (p_username, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE loophz(usernames TEXT[], phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(usernames,1) LOOP
        IF phones[i] ~ '^[0-9+]+$' THEN
            CALL upsert_u(usernames[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: % for user %', phones[i], usernames[i];
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE del_user(p_username VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_username IS NOT NULL AND username = p_username)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;