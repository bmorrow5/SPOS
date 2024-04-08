-- Create employee data
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
    email_type VARCHAR(50) NOT NULL
);


-- Players and game
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
CREATE TABLE IF NOT EXISTS spos.negotiation_games (
    game_id SERIAL PRIMARY KEY,
    buyer_agent_id INT NOT NULL,
    seller_id INT NOT NULL,
    network_id INT NOT NULL,
    seller_negotiation_power FLOAT,
    buyer_negotiation_power FLOAT,
    initial_price DECIMAL NOT NULL,
    counter_price DECIMAL,
    final_price DECIMAL,
    status VARCHAR(50), -- 'in_progress', 'completed'
    FOREIGN KEY (buyer_agent_id) REFERENCES spos.buyer_agents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES spos.sellers(seller_id)
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
CREATE TABLE IF NOT EXISTS spos.bayesian_networks (
    network_id SERIAL PRIMARY KEY,
    type VARCHAR(255) NOT NULL, -- 'buyer' or 'supplier'
    value DECIMAL NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Bayesian network data
/* The MAIN NODE labels indicate our three parent nodes that contribute directly to the 
Buyer or seller negotiating power, and are required at a minimum for our network. 
*/

-- Buyer Nodes

-- MAIN BUYER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.buyer_capability (
    id INT SERIAL PRIMARY KEY,
    buyer_agent_id INT NOT NULL,
    network_id INT NOT NULL,
    past_project_performance VARCHAR(255),
    qualifications VARCHAR(255),
    certifications VARCHAR(255),
    capacity_metrics VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- buyer_capability parent node
CREATE TABLE IF NOT EXISTS spos.buyer_payment_status (
    id INT SERIAL PRIMARY KEY,
    buyer_agent_id INT NOT NULL,
    network_id INT NOT NULL,
    historical_payment_records VARCHAR(255),
    average_time_to_payment INT,
    number_of_delayed_payments INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- buyer_capability parent node
CREATE TABLE IF NOT EXISTS spos.benefit_after_deal (
    id INT SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    network_id INT NOT NULL,
    profit_margin DECIMAL(10, 2),
    market_growth_projection DECIMAL(5, 2),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);



-- MAIN BUYER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.market_competition (
    id INT SERIAL PRIMARY KEY,
    market_id INT NOT NULL,
    network_id INT NOT NULL,
    number_and_size_of_competitors VARCHAR(255),
    market_share_data DECIMAL(5, 2),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- market_competition parent node
CREATE TABLE IF NOT EXISTS spos.estimated_direct_costs (
    id INT SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    network_id INT NOT NULL,
    previous_project_budget DECIMAL(10, 2),
    current_cost_estimate DECIMAL(10, 2),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- market_competition_parent node
CREATE TABLE IF NOT EXISTS spos.number_suppliers (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    number_of_suppliers INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- market_competition_parent node
CREATE TABLE IF NOT EXISTS spos.market_price_fluctuation (
    id INT SERIAL PRIMARY KEY,
    market_id INT NOT NULL,
    network_id INT NOT NULL,
    commodity_prices DECIMAL(10, 2),
    seasonal_and_trend_analysis VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- market_price_fluction parent node AND seller economic stability/prodcution_cost parent node
CREATE TABLE IF NOT EXISTS spos.inflation (
    id INT SERIAL PRIMARY KEY,
    network_id INT NOT NULL,
    date DATE NOT NULL,
    historical_inflation_rate DECIMAL(5, 2)
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- market_price_fluctuation parent node
CREATE TABLE IF NOT EXISTS spos.bank_interest_rate (
    id INT SERIAL PRIMARY KEY,
    network_id INT NOT NULL,
    date DATE NOT NULL,
    central_bank_report VARCHAR(255),
    financial_market_data DECIMAL(5, 2)
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);



-- MAIN BUYER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.negotiation_deadline_pressure (
    id INT SERIAL PRIMARY KEY,
    negotiation_id INT NOT NULL,
    historical_negotiation_timelines INT,
    time_sensitivity_of_project_delivery VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
--benefit_after_deal AND negotiation_deadline_pressure parent node
CREATE TABLE IF NOT EXISTS spos.offer_price (
    id INT SERIAL PRIMARY KEY,
    offer_id INT NOT NULL,
    previous_bidding_prices DECIMAL(10, 2),
    market_analysis VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- negotiation_deadline_pressure parent node
CREATE TABLE IF NOT EXISTS spos.current_negotiation_time (
    id INT SERIAL PRIMARY KEY,
    negotiation_id INT NOT NULL,
    ongoing_negotiation_duration INT,
    historical_negotiation_length INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);




-- Seller Node data

-- MAIN SELLER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.competition_capability (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    competitive_analysis VARCHAR(255),
    swot_analysis TEXT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- competition_capability parent node
CREATE TABLE IF NOT EXISTS spos.production_costs (
    id INT SERIAL PRIMARY KEY,
    network_id INT NOT NULL,
    production_costs INT NOT NULL,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- production_costs, stability_level parent node
CREATE TABLE IF NOT EXISTS spos.inflation_cost (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    cost_breakdown VARCHAR(255),
    time_series_data VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- compeitition_capability parent node
CREATE TABLE IF NOT EXISTS spos.number_competitors (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    number_of_suppliers INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- competition_capability, negotiation_pressure parent node
CREATE TABLE IF NOT EXISTS spos.overheads (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    overhead_costs DECIMAL(10, 2),
    cost_accounting_reports VARCHAR(255),
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);



-- MAIN SELLER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.negotiation_deadline_pressure (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    number_of_suppliers INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);





-- MAIN SELLER POWER PARENT NODE 
CREATE TABLE IF NOT EXISTS spos.stability_level_of_economy (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    stability_level INT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);
-- Parent node of stability_level_of_economy
CREATE TABLE IF NOT EXISTS spos.competition_of_market_price (
    id INT SERIAL PRIMARY KEY,
    supplier_id INT NOT NULL,
    network_id INT NOT NULL,
    opponent_prices FLOAT,
    FOREIGN KEY (network_id) REFERENCES spos.bayesian_networks(network_id)
);