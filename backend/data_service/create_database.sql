-- Create employee data
CREATE SCHEMA IF NOT EXISTS spos
    AUTHORIZATION postgres;

-- Players and game
CREATE TABLE IF NOT EXISTS spos.sellers (
    seller_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS spos.buyer_agents (
    buyer_agent_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS spos.negotiation_games (
    game_id SERIAL PRIMARY KEY,
    buyer_agent_id INT NOT NULL,
    seller_id INT NOT NULL,
    initial_price DECIMAL NOT NULL,
    counter_price DECIMAL,
    final_price DECIMAL,
    status VARCHAR(50), -- e.g., 'in_progress', 'completed'
    FOREIGN KEY (buyer_agent_id) REFERENCES BuyerAgents(buyer_agent_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id)
);


-- Email storage
CREATE TABLE IF NOT EXISTS EmailLogs (
    email_log_id SERIAL PRIMARY KEY,
    sender_email VARCHAR(255) NOT NULL,
    receiver_email VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email_type VARCHAR(50) NOT NULL
);



-- Network Data
CREATE TABLE IF NOT EXISTS BayesianNetworkData (
    data_id SERIAL PRIMARY KEY,
    type VARCHAR(255) NOT NULL, -- 'buyer' or 'supplier'
    node_name VARCHAR(255) NOT NULL,
    value DECIMAL NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Buyer node data
-- MAIN NODE
CREATE TABLE IF NOT EXISTS BuyerPaymentStatus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    historical_payment_records VARCHAR(255),
    average_time_to_payment INT,
    number_of_delayed_payments INT,
    FOREIGN KEY (buyer_id) REFERENCES Buyers(id)
);

-- MAIN NODE
CREATE TABLE IF NOT EXISTS ContractorCapability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contractor_id INT NOT NULL,
    past_project_performance VARCHAR(255),
    qualifications VARCHAR(255),
    certifications VARCHAR(255),
    capacity_metrics VARCHAR(255),
    FOREIGN KEY (contractor_id) REFERENCES Contractors(id)
);

CREATE TABLE IF NOT EXISTS EstimatedDirectCost (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    previous_project_budget DECIMAL(10, 2),
    current_cost_estimate DECIMAL(10, 2),
    FOREIGN KEY (project_id) REFERENCES Projects(id)
);

CREATE TABLE IF NOT EXISTS BenefitAfterDeal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    profit_margin DECIMAL(10, 2),
    market_growth_projection DECIMAL(5, 2),
    FOREIGN KEY (project_id) REFERENCES Projects(id)
);

CREATE TABLE IF NOT EXISTS OfferPrice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    offer_id INT NOT NULL,
    previous_bidding_prices DECIMAL(10, 2),
    market_analysis VARCHAR(255),
    FOREIGN KEY (offer_id) REFERENCES Offers(id)
);

CREATE TABLE IF NOT EXISTS NegotiationDeadlinePressure (
    id INT AUTO_INCREMENT PRIMARY KEY,
    negotiation_id INT NOT NULL,
    historical_negotiation_timelines INT,
    time_sensitivity_of_project_delivery VARCHAR(255),
    FOREIGN KEY (negotiation_id) REFERENCES Negotiations(id)
);

CREATE TABLE IF NOT EXISTS MarketCompetition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    market_id INT NOT NULL,
    number_and_size_of_competitors VARCHAR(255),
    market_share_data DECIMAL(5, 2),
    FOREIGN KEY (market_id) REFERENCES Markets(id)
);

CREATE TABLE IF NOT EXISTS Inflation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year YEAR NOT NULL,
    historical_inflation_rate DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS FluctuationOfMarketPrice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    market_id INT NOT NULL,
    commodity_prices DECIMAL(10, 2),
    seasonal_and_trend_analysis VARCHAR(255),
    FOREIGN KEY (market_id) REFERENCES Markets(id)
);

CREATE TABLE IF NOT EXISTS BankInterestRate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    central_bank_report VARCHAR(255),
    financial_market_data DECIMAL(5, 2)
);

CREATE TABLE IF NOT EXISTS CurrentNegotiationTime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    negotiation_id INT NOT NULL,
    ongoing_negotiation_duration INT,
    historical_negotiation_length INT,
    FOREIGN KEY (negotiation_id) REFERENCES Negotiations(id)
);

-- Seller Node data
CREATE TABLE IF NOT EXISTS ProductionCost (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    cost_breakdown VARCHAR(255),
    time_series_data VARCHAR(255),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
);

CREATE TABLE IF NOT EXISTS CompetitionCapability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    competitive_analysis VARCHAR(255),
    swot_analysis TEXT,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
);

CREATE TABLE IF NOT EXISTS NoOfCompetitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    number_of_suppliers INT,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
);

CREATE TABLE IF NOT EXISTS Overheads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    overhead_costs DECIMAL(10, 2),
    cost_accounting_reports VARCHAR(255),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
);