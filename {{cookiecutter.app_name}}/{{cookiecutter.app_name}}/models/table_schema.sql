CREATE TABLE users (
    uid SERIAL PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL);

-- test row users
INSERT INTO users (
    username,
    first_name,
    last_name,
    password,
    email
) VALUES (
    'bfulroth',
    'Ben',
    'Fulroth',
    'pass123',
    'ben@test.com'
);

INSERT INTO skin_users (
    username,
    first_name,
    last_name,
    password,
    email
) VALUES (
    'andrewchang',
    'Andrew',
    'Chang',
    'password',
    'andrew@test.com'
);

-- test row images_users
INSERT INTO images_users (
    user_id,
    image_location
) VALUES (
    1, -- Tony has user_id of 1
    'https://ucarecdn.com/bfaa3806-81b4-434b-8dac-e438442feead/'
);

INSERT INTO images_users (
    user_id,
    image_location
) VALUES (
    2, -- Andrew has user_id of 1
    'https://ucarecdn.com/9acea333-adfa-4dfd-a207-0bf80588b1cc/'
);