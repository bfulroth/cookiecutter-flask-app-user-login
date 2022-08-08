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