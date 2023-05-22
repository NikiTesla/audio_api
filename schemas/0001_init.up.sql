CREATE TABLE IF NOT EXISTS users(
    id serial PRIMARY KEY,
    username VARCHAR(255),
    token VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS audio_table (
    id serial PRIMARY KEY,
    -- audio BINARY
);