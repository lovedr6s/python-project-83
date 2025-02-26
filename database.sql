CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp);

CREATE TABLE url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);