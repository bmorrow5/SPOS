
--Create database
-- CREATE DATABASE default_company;

-- Create schema
CREATE SCHEMA IF NOT EXISTS spos
    AUTHORIZATION postgres;

-- Players and products
CREATE TABLE IF NOT EXISTS spos.sellers (
    seller_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS spos.buyer_agents (
    buyer_agent_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    employee_id INT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL --Needs to be encrypted before storage
);
CREATE TABLE IF NOT EXISTS spos.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    quantity INT NOT NULL,
    max_price FLOAT NOT NULL,
    date_needed_by DATE NOT NULL,
    UNIQUE(name, quantity, max_price, date_needed_by) -- This will prevent duplicate rows
    );

-- Store games
-- I know this table is not in normal form, I will fix it when able
CREATE TABLE IF NOT EXISTS spos.games (
    game_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL,
    buyer_agent_id INT NOT NULL,
    product_id INT NOT NULL,
    buyer_power INT, 
    seller_power INT,
    initial_price FLOAT, 
    current_price FLOAT,
    last_seller_price FLOAT, 
    last_buyer_price FLOAT, 
    buyer_reservation_price FLOAT,
    seller_reservation_price FLOAT,
    buyer_deadline DATE,
    seller_deadline DATE,
    current_strategy VARCHAR(255),
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,
    FOREIGN KEY (buyer_agent_id) REFERENCES spos.buyer_agents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES spos.sellers(seller_id),
    FOREIGN KEY (product_id) REFERENCES spos.products(product_id)
);
-- Email storage
CREATE TABLE IF NOT EXISTS spos.email_logs (
    email_log_id SERIAL PRIMARY KEY,
    sender_email VARCHAR(255) NOT NULL,
    receiver_email VARCHAR(255) NOT NULL,
    buyer_agent_id INT,
    seller_id INT,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_agent_id) REFERENCES spos.buyer_agents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES spos.sellers(seller_id)
);

-- Insert test data

-- Insert test data into sellers
INSERT INTO spos.sellers (first_name, last_name, email)
VALUES ('Brandon', 'Morrow', 'brandonmorrow09@gmail.com');

-- Insert test data into buyer_agents
INSERT INTO spos.buyer_agents (first_name, last_name, employee_id, email, password)
VALUES ('John', 'Doe', 1011001, 'spos6045@gmail.com', '$2b$12$QjgW/mYz26HV0iANfeWk1e1LSFD1GSQiy2SZHJawCU87kyowKUnpi');

-- Insert test data into products
INSERT INTO spos.products (name, quantity, max_price, date_needed_by)
VALUES ('Office Chair', 100, 50.0, '2023-12-31');

-- Insert test data into games
INSERT INTO spos.games (seller_id, buyer_agent_id, product_id, buyer_power, seller_power, initial_price, current_price, last_seller_price, buyer_reservation_price, seller_reservation_price, start_date, buyer_deadline, current_strategy)
VALUES (1, 1, 1, 0, 0, 1000.00, 1000.00, 1000.00, 800.00, 400.00, '2024-04-15', '2024-05-20', 'conciliatory'); 

-- Insert test data into email_logs
INSERT INTO spos.email_logs (sender_email, receiver_email, buyer_agent_id, seller_id, subject, body)
VALUES ('spos6045@gmail.com', 'brandonmorrow09@gmail.com', 1, 1, 'Test Email Subject', 'This is a test email body.');
