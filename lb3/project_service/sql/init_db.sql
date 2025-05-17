CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_projects_name ON projects (name);

INSERT INTO public.projects (name, description) VALUES
('Project1', 'Description1'),
('Project2', 'Description2'),
('Project3', 'Description3'),
('Project4', 'Description4'),
('Project5', 'Description5')
