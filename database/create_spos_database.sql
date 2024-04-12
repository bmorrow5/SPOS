
--Create database
CREATE DATABASE IF NOT EXISTS default_company;

-- Create schema
CREATE SCHEMA IF NOT EXISTS spos
    AUTHORIZATION postgres;

-- Email storage
CREATE TABLE IF NOT EXISTS spos.email_logs (
    email_log_id SERIAL PRIMARY KEY,
    sender_email VARCHAR(255) NOT NULL,
    receiver_email VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

-- Players and products
CREATE TABLE IF NOT EXISTS spos.sellers (
    seller_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS spos.buyer_agents (
    buyer_agent_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL --Needs to be encrypted before storage
);
CREATE TABLE IF NOT EXISTS spos.products (
    product_id SERIAL PRIMARY KEY,
    buyer_agent_id INT NOT NULL,
    seller_id INT NOT NULL,
    quantity INT NOT NULL,
    max_price FLOAT NOT NULL,
    date_needed_by DATE NOT NULL,
    FOREIGN KEY (buyer_agent_id) REFERENCES spos.buyer_agents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES spos.sellers(seller_id)
);

-- Store games
CREATE TABLE IF NOT EXISTS spos.games {
    game_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL,
    buyer_agent_id INT NOT NULL,
    product_id INT NOT NULL,
    buyer_power INT, -- Buyer negotiation power
    seller_power INT, -- Seller negotiation power
    buyer_reservation_price FLOAT,
    seller_reservation_price FLOAT,
    current_strategy VARCHAR(255),
    FOREIGN KEY (buyer_agent_id) REFERENCES spos.buyer_agents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES spos.sellers(seller_id),
    FOREIGN KEY (product_id) REFERENCES spos.products(product_id)
};


-- Insert test data

-- Insert test data into email_logs
INSERT INTO spos.email_logs (sender_email, receiver_email, subject, body, email_type)
VALUES ('spos@gmail.com', 'brandonmorrow09@gmail.com', 'Test Email Subject', 'This is a test email body.');

-- Insert test data into sellers
INSERT INTO spos.sellers (name, email)
VALUES ('Seller One', 'seller1@company.com');

-- Insert test data into buyer_agents
INSERT INTO spos.buyer_agents (employee_id, email, password)
VALUES (101001, 'buyer1@company.com', 'encrypted_password_here');

-- Insert test data into products
INSERT INTO spos.products (buyer_agent_id, seller_id, quantity, max_price, date_needed_by)
VALUES (1, 1, 100, 50.0, '2023-12-31');

-- Insert test data into games
INSERT INTO spos.games (seller_id, buyer_agent_id, product_id, buyer_power, seller_power, buyer_reservation_price, seller_reservation_price, current_strategy)
VALUES (1, 1, 1, 50, 50, 45.0, 55.0, 'conciliatory'); 