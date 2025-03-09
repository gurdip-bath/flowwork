-- create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create departments table first, but with a placeholder for manager_id
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    manager_id INTEGER -- added the foreign key restraint below
);

-- Create employees tables
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(50),
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    position VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'active'
);

-- Now add the foreign key constraint to departments table
ALTER TABLE departments 
ADD CONSTRAINT fk_manager_id 
FOREIGN KEY (manager_id) REFERENCES employees(id) ON DELETE SET NULL;

-- Create onboarding table
CREATE TABLE onboarding (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL UNIQUE REFERENCES employees(id) ON DELETE CASCADE,
    employee_start_date DATE NOT NULL,
    employee_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    offer_letter_url VARCHAR(255),
    contract_status VARCHAR(50) NOT NULL DEFAULT 'unsigned',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_onboarding_status ON onboarding(status);

-- Insert initial departments
INSERT INTO departments (name, description)
VALUES 
    ('Human Resources', 'Responsible for recruiting and employee management'),
    ('Engineering', 'Software development and technical operations'),
    ('Administration', 'Office and business administration');