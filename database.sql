CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at DATE,
    status_code INTEGER);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at DATE
);