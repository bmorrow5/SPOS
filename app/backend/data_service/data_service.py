import sys
import os
# Add the current directory to the path so that the models can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)
import bcrypt
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, SellerDatabase, BuyerAgentDatabase, ProductDatabase, GameDatabase, EmailLogDatabase
from sqlalchemy.exc import SQLAlchemyError

# Add the current directory to the path so that the models can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, current_dir)


class DataService():
    """This class serves as the data service for the application, and will perform CRUD operations on all database tables
    """

    def __init__(self, engine_url='postgresql://postgres:spos123@localhost:5432/default_company'):
        self.engine = create_engine(engine_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    ############## Password Handling ##############
    def encrypt_password(password):
        # Convert the password to a byte string
        byte_password = password.encode()
        # Generate a salt and hash the password
        hashed = bcrypt.hashpw(byte_password, bcrypt.gensalt())
        return hashed.decode()  # decode the hash to store in the database as a string

    
    @staticmethod
    def verify_user(email, password):
        """Verifies the user by checking the email and password
        """
        session = None
        try:
            ds = DataService()
            session = ds.Session()
            user = session.query(BuyerAgentDatabase).filter_by(email=email).one_or_none()
            if user:
                byte_password = password.encode()
                if bcrypt.checkpw(byte_password, user.password.encode()):
                    return True
            return False
        except SQLAlchemyError as e:
            logging.error(f"Error verifying user: {e}")
            return False
        finally:
            session.close()



    ############## Seller CRUD ##############
    def create_seller(self, first_name, last_name, email):
        try: 
            with self.Session() as session:
                new_seller = SellerDatabase(first_name=first_name, last_name=last_name, email=email)
                session.add(new_seller)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing seller: {e}")

    def read_seller(self, seller_id=None, first_name=None, last_name=None, email=None):
        try:
            with self.Session() as session:
                if seller_id:
                    return session.query(SellerDatabase).filter_by(seller_id=seller_id).one_or_none()
                elif first_name and last_name:
                    return session.query(SellerDatabase).filter_by(first_name=first_name, last_name=last_name).one_or_none()
                elif email:
                    return session.query(SellerDatabase).filter_by(email=email).one_or_none()
                else:
                    return None
        except SQLAlchemyError as e:
            logging.error(f"Error Reading seller: {e}")

    def read_all_sellers(self):
        try:
            with self.Session() as session:
                sellers = session.query(SellerDatabase).all()
            sellers_dict = {seller.seller_id: {"first_name": seller.first_name, 
                                                "last_name": seller.last_name,
                                                "email": seller.email} for seller in sellers}
            return sellers_dict
        except SQLAlchemyError as e:
            logging.error(f"Error Reading seller: {e}")

        
    def update_seller_email(self, first_name=None, last_name=None, email=None):
        try:
            with self.Session() as session:
                seller =  session.query(SellerDatabase).filter_by(first_name=first_name, last_name=last_name).one_or_none()
                if email:
                    seller.email = email
                session.commit()
                return seller
        except SQLAlchemyError as e:
            logging.error(f"Error updating seller email: {e}")


    def delete_seller(self, first_name=None, last_name=None, email=None):
        try:
            with self.Session() as session:
                if first_name and last_name:
                    seller = session.query(SellerDatabase).filter_by(first_name=first_name, last_name=last_name).one_or_none()
                elif email:
                    seller = session.query(SellerDatabase).filter_by(email=email).one_or_none()
                if seller:
                    session.delete(seller)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error deleting seller: {e}")
    
    
    ############## Buyer CRUD ##############
    def create_buyer(self, first_name, last_name, employee_id, email, password):
        try:
            password = self.encrypt_password(password) # Encrypt the password before storage
            with self.Session() as session:
                new_buyer = BuyerAgentDatabase(first_name=first_name, last_name=last_name, employee_id = employee_id, email=email, password=password)
                session.add(new_buyer)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing buying: {e}")


    def read_buyer(self, first_name=None, last_name=None, employee_id=None, email=None, password=None):
        """Can take any buyer identifier and will pull their information
        """
        try:
            with self.Session() as session:
                if first_name and last_name:
                    return session.query(BuyerAgentDatabase).filter_by(first_name=first_name, last_name=last_name).one_or_none()
                elif employee_id:
                    return session.query(BuyerAgentDatabase).filter_by(employee_id=employee_id).one_or_none()
                elif email:
                    buyer = session.query(BuyerAgentDatabase).filter_by(email=email).one_or_none()
                    return {"buyer_agent_id": buyer.buyer_agent_id, "first_name": buyer.first_name, "last_name": buyer.last_name, "email": buyer.email}
                elif password:
                    return session.query(BuyerAgentDatabase).filter_by(password=password).one_or_none()
                else:
                    return None
        except SQLAlchemyError as e:
            logging.error(f"Error reading buyer: {e}")


    def update_buyer(self, buyer_id, **kwargs):
        """Note: Requires the buyer_id to be passed in as a keyword argument"""
        try:
            with self.Session() as session:
                # Retrieve the buyer by ID
                buyer = session.query(BuyerAgentDatabase).filter_by(buyer_agent_id=buyer_id).one_or_none()
                if buyer:
                    # Update attributes that are provided in kwargs and exist in the BuyerAgentDatabase model.
                    valid_keys = {column.name for column in BuyerAgentDatabase.__table__.columns}
                    for key, value in kwargs.items():
                        if key in valid_keys:
                            setattr(buyer, key, value)
                        else:
                            logging.warning(f"Attempted to update non-existent attribute '{key}'")
                    session.commit()
                    return buyer
                else:
                    logging.error(f"No buyer found with ID: {buyer_id}")
                    return None
        except SQLAlchemyError as e:
            logging.error(f"Error updating buyer: {e}")
            return None


    def delete_buyer(self, buyer_id):
        try:
            with self.Session() as session:
                buyer = session.query(BuyerAgentDatabase).filter_by(buyer_id=buyer_id).one_or_none()
                if buyer:
                    session.delete(buyer)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error deleting buyer: {e}")

        
    ############## Product CRUD ##############
    def create_product(self, name, quantity, max_price, date_needed_by):
        try:
            with self.Session() as session:
                new_product = ProductDatabase(
                    name=name,
                    quantity=quantity,
                    max_price=max_price,
                    date_needed_by=date_needed_by
                )
                session.add(new_product)
                session.commit()
                product_id = new_product.product_id
            return {"product_id": product_id,
                    "name": name, 
                    "quantity": quantity, 
                    "max_price": max_price, 
                    "date_needed_by": date_needed_by}
        except SQLAlchemyError as e:
            logging.error(f"Error storing product: {e}")


    def read_product(self, product_id):
        try:
            with self.Session() as session:
                product_obj = session.query(ProductDatabase).filter_by(product_id=product_id).one()

                product_dict = {"product_id": product_obj.product_id,
                                "name": product_obj.name,
                                "quantity": product_obj.quantity,
                                "max_price": product_obj.max_price,
                                "date_needed_by": product_obj.date_needed_by}
                return product_dict
        except SQLAlchemyError as e:
            logging.error(f"Error reading product: {e}")


    def update_product(self, product_id, new_quantity=None, new_max_price=None, new_date_needed_by=None):
        try:
            with self.Session() as session:
                products = session.query(ProductDatabase).filter_by(product_id).all()
                for product in products:
                    if new_quantity:
                        product.quantity = new_quantity
                    if new_max_price:
                        product.max_price = new_max_price
                    if new_date_needed_by:
                        product.date_needed_by = new_date_needed_by
                session.commit()
                return products
        except SQLAlchemyError as e:
            logging.error(f"Error updating product: {e}")


    def delete_product(self, product_id):
        try:
            with self.Session() as session:
                products = session.query(ProductDatabase).filter_by(product_id).all()
                for product in products:
                    session.delete(product)
                session.commit()
                return True
        except SQLAlchemyError as e:
            logging.error(f"Error deleting product: {e}")

    ############## Game CRUD ##############
    def create_game(self, seller_id, buyer_agent_id, product_id, buyer_power=None, seller_power=None, buyer_reservation_price=None, start_date=None, seller_reservation_price=None, current_strategy=None, buyer_deadline=None):
        try:
            with self.Session() as session:
                new_game = GameDatabase(
                    seller_id=seller_id,
                    buyer_agent_id=buyer_agent_id,
                    product_id=product_id,
                    buyer_power=buyer_power,
                    seller_power=seller_power,
                    buyer_reservation_price=buyer_reservation_price,
                    seller_reservation_price=seller_reservation_price,
                    current_strategy=current_strategy,
                    start_date=start_date,
                    buyer_deadline=buyer_deadline,
                )
                session.add(new_game)
                session.commit()
                game_id = new_game.game_id
            return game_id
        except SQLAlchemyError as e:
            logging.error(f"Error storing game: {e}")


    def read_game(self, game_id):
        try:
            with self.Session() as session:
                game = session.query(GameDatabase).filter_by(game_id=game_id).one_or_none()
                game_dict = {"game_id": game.game_id,
                                "seller_id": game.seller_id,
                                "buyer_agent_id": game.buyer_agent_id,
                                "product_id": game.product_id,
                                "buyer_power": game.buyer_power,
                                "seller_power": game.seller_power,
                                "current_strategy": game.current_strategy,
                                "initial_price": game.initial_price,
                                "current_price": game.current_price,
                                "last_seller_price": game.last_seller_price,
                                "last_buyer_price": game.last_buyer_price,                                
                                "buyer_reservation_price": game.buyer_reservation_price,
                                "seller_reservation_price": game.seller_reservation_price,
                                "buyer_deadline": game.buyer_deadline,
                                "seller_deadline": game.seller_deadline,
                                "start_date": game.start_date
                                }
                return game_dict
        except SQLAlchemyError as e:
            logging.error(f"Error reading game: {e}")

    def read_all_games(self):
        try:
            with self.Session() as session:
                games = session.query(GameDatabase).join(BuyerAgentDatabase).join(SellerDatabase).join(ProductDatabase).all()
                games_dict = {}
                for game in games:
                    games_dict[game.game_id] = {"game_id": game.game_id,
                                                "product_name": game.product.name,
                                                "product_quantity": game.product.quantity,
                                                "buyer_max_price": game.buyer_reservation_price,
                                                "initial_price": game.initial_price,
                                                "current_price": game.current_price,
                                                "last_seller_price": game.last_seller_price,
                                                "last_buyer_price": game.last_buyer_price,     
                                                "negotiation_start_date": game.start_date,
                                                "buyer_deadline": game.buyer_deadline,
                                                "seller_first_name": game.seller.first_name,
                                                "seller_last_name": game.seller.last_name,
                                                "seller_email": game.seller.email,
                                                "buyer_power": game.buyer_power,
                                                "seller_power": game.seller_power,
                                                "current_strategy": game.current_strategy                           
                                                }
                return games_dict
        except SQLAlchemyError as e:
            logging.error(f"Error Reading seller: {e}")


    def update_game(self, game_id, **kwargs):
        try:
            if game_id:
                with self.Session() as session:
                    game = session.query(GameDatabase).filter_by(game_id=game_id).one_or_none()
                    if game:
                        valid_keys = {c.name for c in GameDatabase.__table__.columns}
                        for key, value in kwargs.items():
                            if key in valid_keys:
                                setattr(game, key, value)
                            else:
                                logging.warning(f"Tried to update invalid attribute '{key}'")
                        session.commit()
                        return game
                    else:
                        logging.info(f"No game found with ID {game_id}")
                        return None
        except SQLAlchemyError as e:
            logging.error(f"Error updating game: {e}")


    def delete_game(self, product_id):
        try:
            with self.Session() as session:
                game = session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()
                if game:
                    session.delete(game)
                    session.commit()
                    return True
        except SQLAlchemyError as e:
            logging.error(f"Error deleting game: {e}")

                
    ############## EmailLog CRUD ##############
    def create_email_log(self, sender_email, receiver_email, subject, body, buyer_agent_id=None, seller_id=None):
        try:
            with self.Session() as session:
                new_email_log = EmailLogDatabase(
                    sender_email=sender_email,
                    receiver_email=receiver_email,
                    subject=subject,
                    body=body,
                    buyer_agent_id=buyer_agent_id,
                    seller_id=seller_id
                )
                session.add(new_email_log)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing emails: {e}")


    def read_email_logs_by_sender(self, sender_email):
        try:
            with self.Session() as session:
                return session.query(EmailLogDatabase).filter_by(sender_email=sender_email).all()
        except SQLAlchemyError as e:
            logging.error(f"Error reading emails from sender: {e}")


    def read_email_logs_by_receiver(self, receiver_email):
        try:
            with self.Session() as session:
                return session.query(EmailLogDatabase).filter_by(receiver_email=receiver_email).all()
        except SQLAlchemyError as e:
            logging.error(f"Error reading emails from receiver: {e}")


    def update_email_log(self, email_log_id, new_subject=None, new_body=None):
        try:
            with self.Session() as session:
                email_log = session.query(EmailLogDatabase).filter_by(email_log_id=email_log_id).one_or_none()
                if email_log:
                    if new_subject:
                        email_log.subject = new_subject
                    if new_body:
                        email_log.body = new_body
                    session.commit()
                    return email_log
        except SQLAlchemyError as e:
            logging.error(f"Error updating email logs: {e}")


    def delete_email_log(self, email_log_id):
        try:
            with self.Session() as session:
                email_log = session.query(EmailLogDatabase).filter_by(email_log_id=email_log_id).one_or_none()
                if email_log:
                    session.delete(email_log)
                    session.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error deleting email: {e}")

        
if __name__== "__main__":
    print("Data Service Running...")