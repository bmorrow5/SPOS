import re
import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from backend.bayesian_fuzzy_game.bayesian_network import GameBayesianNetwork
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService

class Main():

    def __init__(self, user_email, user_password):
        # Start services
        data_service = DataService()
        buyer = data_service.read_buyer(email= user_email)
        first_name = buyer['first_name']
        last_name = buyer['last_name']
        email_service = EmailService(email= user_email, password=user_password)
        
        self.user_email = user_email
        self.user_password = user_password
        self.first_name = first_name
        self.last_name = last_name
        self.data_service = data_service
        self.email_service = email_service


    ############## New Game Request Quotes ############## 
    def update_game_app(self, game_id, seller_counteroffer, bayesian_network_variable_dict=None):
        # Add new counteroffer to database
        # key_values = {'game_id': game_id, 'last_seller_price': seller_counteroffer}
        self.data_service.update_game(game_id=game_id, last_seller_price=seller_counteroffer)

        # Get the game from the database
        old_game = self.data_service.read_game(game_id=game_id)

        game_time_days = datetime.now().date() - old_game['start_date']
        game_time_days = game_time_days.days

        negotiation_length = old_game['buyer_deadline'] - old_game['start_date']
        negotiation_length = negotiation_length.days
        # print(negotiation_length, game_time_days)


        # Get product information
        read_product = self.data_service.read_product(product_id=old_game['product_id'])
        old_game['name'] = read_product['name']
        old_game['product_quantity'] = read_product['quantity']

        # Get Seller information
        read_seller = self.data_service.read_seller(seller_id=old_game['seller_id'])
        seller_name = read_seller.first_name + " " + read_seller.last_name
        seller_email = read_seller.email

        # Declare the product, buyer, and seller
        product = {'name': old_game['name'], 
                   'quantity': old_game['product_quantity'], 
                   'initial_price': old_game['initial_price'], 
                   'current_price': old_game['current_price']}

        buyer = {'name': self.first_name + " " + self.last_name, 
                 'email': self.user_email, 
                 'negotiation_power': old_game['buyer_power'], 
                 'reservation_price': old_game['buyer_reservation_price'], 
                 'last_offer_price': old_game['last_buyer_price'],
                 'deadline': old_game['buyer_deadline']}
        
        seller = {'name': seller_name, 
                  'email': seller_email, 
                  'negotiation_power': old_game['seller_power'], 
                  'reservation_price': old_game['seller_reservation_price'], 
                  'last_offer_price': old_game['last_seller_price'],
                  'deadline': old_game['seller_deadline']}


        # Update the game
        # game_time_days, product, buyer, seller, bayesian_network_variable_dict
        bayesian_game = BayesianFuzzyGame(negotiation_length=negotiation_length,
                                          game_time_days=game_time_days, 
                                          product=product, 
                                          buyer=buyer, 
                                          seller=seller, 
                                          bayesian_network_variable_dict=bayesian_network_variable_dict)
        
        # Perform the game theory calculations, and return updated game values
        game_dict = bayesian_game.update_game()
        # print(game_dict)
        # Store our counteroffer value in the database
        self.data_service.update_game(game_id=game_id, 
                                      buyer_power=game_dict['buyer_utility'], 
                                      seller_power=game_dict['seller_utility'], 
                                      current_price=game_dict['current_price'],
                                      current_strategy=game_dict['current_strategy'],
                                      last_buyer_price=game_dict['counter_offer_price'], 
                                      last_seller_price=game_dict['last_seller_price']  
                                      )
        if game_dict['initial_price'] is not None:
            self.data_service.update_game(game_id=game_id, initial_price=game_dict['initial_price'])


        # Get the counteroffer price
        counter_offer_price = game_dict['counter_offer_price']
        return counter_offer_price
        


    ############## New Game - Email Sellers Requesting Quotes ############## 
    def request_quotes(self, product_name, product_quantity, product_max_price, date_needed_by, message=None):
        try:
            
            # Create a new product, get sellers and current user
            product = self.data_service.create_product(name=product_name, quantity=product_quantity, max_price=product_max_price, date_needed_by=date_needed_by)
            sellers_dict = self.data_service.read_all_sellers()
            buyer_dict = self.data_service.read_buyer(email= self.user_email)

            # If message is none make a custom message for each seller
            if message is None:
                message = f"We are requesting a quote for {product['quantity']} {product['name']}.\n\nPlease reply to this email with your best price, and in the body of the email, not on an attachment."
            
            email_results = []
            # Iterate through all sellers in the database, create a game and send an email request for quote
            for seller_id, seller_info in sellers_dict.items():
                game_id = self.data_service.create_game(seller_id = seller_id, 
                                      buyer_agent_id = buyer_dict['buyer_agent_id'], 
                                      product_id= product['product_id'], 
                                      buyer_reservation_price= (product['quantity'] * product['max_price']), # Total price
                                      start_date = datetime.now().date(),
                                      buyer_deadline = date_needed_by,
                                      buyer_power=0,
                                      seller_power=0
                                      )
                
                greeting = f"Hello {seller_info['first_name']} {seller_info['last_name']},"
                farewell = f"Thank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
                final_message = f"{greeting}\n\n{message}\n\n{farewell}"
                subject = f"Request for Quote - {product['quantity']} {product['name']} - Request ID: ({game_id})"
                try:
                    self.email_service.send_emails(to_emails= [seller_info['email']], subject=subject, message=final_message)
                    # email_results.append(f"Seller ({seller_id}) - Request for quotes sent \t")
                except Exception as e:
                    email_results.append(f"Seller({seller_id}) - Failed to send email: {e}")
            return email_results
        except Exception as e:
             return f"Failed to create game: {e}"

    ############## Add Seller Form ##############     
    def add_seller_to_database(self, first_name, last_name, email):
        try:
            # Create a new seller
            self.data_service.create_seller(first_name=first_name, last_name=last_name, email=email)
            return f"Added Seller: {first_name} {last_name}"
        except Exception as e:
            return f"Failed to add seller: {e}"
    

    ############## Get All Games for Game Table ############## 
    def get_game_table_data(self):
        """This will return a plot of the top sellers
        """
        data = self.data_service.read_all_games()
        return data
    
    ############## Plot Buyer Network ############## 
    def get_buyer_network(self):
        game_network = GameBayesianNetwork()
        game_network.create_buyer_network()
        buyer_network = game_network.buyer_network
        G = nx.DiGraph(buyer_network.edges())
        # Convert NetworkX graph to Cytoscape compatible elements
        nodes = [{'data': {'id': str(node), 'label': str(node)}} for node in G.nodes()]
        edges = [{'data': {'source': str(source), 'target': str(target)}} for source, target in G.edges()]
        elements = nodes + edges
        return elements


    ############## Plot Seller Network ############## 
    def get_seller_network(self):
        game_network = GameBayesianNetwork()
        game_network.create_seller_network()
        buyer_network = game_network.seller_network
        G = nx.DiGraph(buyer_network.edges())
        # Convert NetworkX graph to Cytoscape compatible elements
        nodes = [{'data': {'id': str(node), 'label': str(node)}} for node in G.nodes()]
        edges = [{'data': {'source': str(source), 'target': str(target)}} for source, target in G.edges()]
        elements = nodes + edges
        return elements


    ############## Read Emails, Send Counteroffers ############## 
    ############## Still working on this automation ##############
    def read_email_and_send_counteroffers(self):
        """Reads emails from the email account and sends counteroffers to the sellers
        """
        print("Reading emails")
        # Get all emails from the email account
        emails = self.email_service.read_emails(type='Unseen') # unseen or all

        # Iterate through all emails
        if emails is None:
            return "No emails to read"
        else:
            for email in emails:
                # subject = email['subject']
                # content = email['content']
                # print(subject, content)
                # Extract game_id and offer price from the email
                # game_id, offer_price = self.extract_game_id_and_price(subject=subject, content=content)
                game_id = 1
                offer_price = 60

                print(game_id, offer_price)
                # Get the game from the database
                game = self.data_service.read_game(game_id=game_id)

                # Get the product from the database
                product = self.data_service.read_product(product_id=game['product_id'])

                # Create a new BayesianFuzzyGame
                # bayesian_game = BayesianFuzzyGame(game=game, product=product)

                # Update the game
                # bayesian_game.update_game()

                # Get the counteroffer price
                # counter_offer_price = bayesian_game.counter_offer_price
                counter_offer_price = 0

                # Send the counteroffer
                # self.send_acceptance(to_email=email['sender_email'], message=f"Counteroffer: {counter_offer_price}")

                # Update the game in the database
                # self.data_service.update_game(game_id=game_id, current_price=counter_offer_price)
                message = f"Counteroffer: {counter_offer_price}"
                reply_subject = f"Re: {email['subject']}"

                self.email_service.send_emails(
                    to_emails=[email['sender_email']],
                    subject=reply_subject,
                    message=message,
                    in_reply_to=email.get('message_id'),  # Ensure to extract and pass the original Message-ID
                    references=email.get('references')  # Pass along existing references
                    )
        return "Emails read and counteroffers sent"
    

    def extract_game_id_and_price(self, subject, content):
        """This will extract the game_id and offer price from the email subject and content using regex

        Args:
            subject (string): Email subject
            content (string): Content of the email

        Returns:
            dict: game_id and offer_price
        """
        # Regex to extract game_id from the subject
        game_id_pattern = r"Request ID: \((\d+)\)"
        # Regex to extract offer_price, $123.45 or 123.45$
        price_pattern = r"\$?(\d+\.\d{2})\$?"

        game_id_match = re.search(game_id_pattern, subject)
        price_match = re.search(price_pattern, content)

        if game_id_match is not None:
            game_id = game_id_match.group(1)
        else:
            game_id = None

        if price_match is not None:
            offer_price = price_match.group(1)
        else:
            offer_price = None

        return {game_id, offer_price}

    ############## Will send acceptance email ############## 
    ############## Will be implemented later ############## 
    def send_acceptance(self, to_email, message):
        """This will send an email accepting the offer

        Args:
            to_email (str): Email to send to
            message (str): Message to send
            original_message_id (str): Original message id

        Returns:
            str: Success or failure message
        """
        message = f"To Whom It May Concern,\n\nThank you for your offer we accept.\n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
        
        self.send_emails(to_emails=[to_email], subject="Acceptance", message=message)


