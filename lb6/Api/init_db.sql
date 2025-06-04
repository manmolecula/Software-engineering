CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);