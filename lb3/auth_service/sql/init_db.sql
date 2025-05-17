CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    initials VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('Guest', 'User', 'Admin')),
    disabled BOOLEAN NOT NULL DEFAULT FALSE,
    password VARCHAR(255) NULL,
    hashed_password  VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);


INSERT INTO public.users (initials, username, role, hashed_password) VALUES
('Fattiakhetdinov Silvestr Dinarovich', 'admin', 'Admin', '$2b$12$Jqb6P.kZtgmXa3rMX3bSzeHqBFWEEtRXnqcQDK7oncBWIZa.cRVmO')
