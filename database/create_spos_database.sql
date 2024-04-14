
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
CREATE TABLE IF NOT EXISTS spos.games (
    game_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL,
    buyer_agent_id INT NOT NULL,
    product_id INT NOT NULL,
    buyer_power INT, -- Buyer negotiation power
    seller_power INT, -- Seller negotiation power
    current_price FLOAT, -- This is the last price in the negotiation
    last_seller_price FLOAT, -- Last price from seller
    last_buyer_price FLOAT, -- Last price from buyer
    buyer_reservation_price FLOAT,
    seller_reservation_price FLOAT,
    current_strategy VARCHAR(255),
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
VALUES ('John', 'Doe', 1011001, 'spos6045@gmail.com', '8c9f5c8b19cad748b5c39b060eaecdda493752598f52ba32a80255350a008dea');

-- Insert test data into products
INSERT INTO spos.products (buyer_agent_id, seller_id, quantity, max_price, date_needed_by)
VALUES (1, 1, 100, 50.0, '2023-12-31');

-- Insert test data into games
INSERT INTO spos.games (seller_id, buyer_agent_id, product_id, buyer_power, seller_power, current_price, last_seller_price, last_buyer_price, buyer_reservation_price, seller_reservation_price, current_strategy)
VALUES (1, 1, 1, 10, 10, 50.0, 50.0, 45.0, 50.0, 55.0, 'conciliatory'); 

-- Insert test data into email_logs
INSERT INTO spos.email_logs (sender_email, receiver_email, buyer_agent_id, seller_id, subject, body)
VALUES ('spos6045@gmail.com', 'brandonmorrow09@gmail.com', 1, 1, 'Test Email Subject', 'This is a test email body.');
