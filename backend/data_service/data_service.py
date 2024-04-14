from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import SellerDatabase, BuyerAgentDatabase, ProductDatabase, GameDatabase, EmailLogDatabase
from sqlalchemy.exc import SQLAlchemyError
import logging


class DataService():
    """This class serves as the data service for the application, and will perform CRUD operations on all database tables
    """

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:spos123@localhost:5432/default_company')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    ############## Seller CRUD ##############
    def create_seller(self, name, email):
        try: 
            with self.Session() as session:
                new_seller = SellerDatabase(name=name, email=email)
                session.add(new_seller)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing seller: {e}")

    def read_seller(self, name=None, email=None):
        try:
            with self.Session() as session:
                if name:
                    return session.query(SellerDatabase).filter_by(name=name).one_or_none()
                elif email:
                    return session.query(SellerDatabase).filter_by(email=email).one_or_none()
                else:
                    return None
        except SQLAlchemyError as e:
            logging.error(f"Error Reading seller: {e}")

    def read_all_sellers():
        pass

        
    def update_seller_email(self, name=None, email=None):
        try:
            with self.Session() as session:
                seller =  session.query(SellerDatabase).filter_by(name=name).one_or_none()
                if email:
                    seller.email = email
                session.commit()
                return seller
        except SQLAlchemyError as e:
            logging.error(f"Error updating seller: {e}")


    def delete_seller(self, name=None, email=None):
        try:
            with self.Session() as session:
                if name:
                    seller = session.query(SellerDatabase).filter_by(name=name).one_or_none()
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
    def create_buyer(self, name, employee_id, email, password):
        try:
            with self.Session() as session:
                new_buyer = BuyerAgentDatabase(name=name, employee_id = employee_id, email=email, password=password)
                session.add(new_buyer)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing buying: {e}")


    def read_buyer(self, name=None, employee_id=None, email=None, password=None):
        """Can take any buyer identifier and will pull their information
        """
        try:
            with self.Session() as session:
                if name:
                    return session.query(BuyerAgentDatabase).filter_by(name=name).one_or_none()
                elif employee_id:
                    return session.query(BuyerAgentDatabase).filter_by(employee_id=employee_id).one_or_none()
                elif email:
                    return session.query(BuyerAgentDatabase).filter_by(email=email).one_or_none()
                elif password:
                    return session.query(BuyerAgentDatabase).filter_by(password=password).one_or_none()
                else:
                    return None
        except SQLAlchemyError as e:
            logging.error(f"Error reading buyer: {e}")


    def update_buyer(self, name=None, employee_id=None, email=None, password=None):
        try:
            with self.Session() as session:
                buyer = session.query(BuyerAgentDatabase).filter_by(name=name).one_or_none()
                if buyer:
                    if name:
                        buyer.name = name
                    if email:
                        buyer.email = email
                    if employee_id:
                        buyer.employee_id = employee_id
                    if password:
                        buyer.password = password
                    session.commit()
                    return buyer
        except SQLAlchemyError as e:
            logging.error(f"Error updating buyer: {e}")


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
    def create_product(self, buyer_agent_id, seller_id, quantity, max_price, date_needed_by):
        try:
            with self.Session() as session:
                new_product = ProductDatabase(
                    buyer_agent_id=buyer_agent_id,
                    seller_id=seller_id,
                    quantity=quantity,
                    max_price=max_price,
                    date_needed_by=date_needed_by
                )
                session.add(new_product)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing product: {e}")


    def read_product(self, buyer_agent_id=None, seller_id=None):
        try:
            with self.Session() as session:
                if buyer_agent_id and seller_id:
                    return session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id, seller_id=seller_id).all()
                elif buyer_agent_id:
                    return session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id).all()
                elif seller_id:
                    return session.query(ProductDatabase).filter_by(seller_id=seller_id).all()
        except SQLAlchemyError as e:
            logging.error(f"Error reading product: {e}")


    def update_product(self, buyer_agent_id, seller_id, new_quantity=None, new_max_price=None, new_date_needed_by=None):
        try:
            with self.Session() as session:
                products = session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id, seller_id=seller_id).all()
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


    def delete_product(self, buyer_agent_id, seller_id):
        try:
            with self.Session() as session:
                products = session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id, seller_id=seller_id).all()
                for product in products:
                    session.delete(product)
                session.commit()
                return True
        except SQLAlchemyError as e:
            logging.error(f"Error deleting product: {e}")

    ############## Game CRUD ##############
    def create_game(self, seller_id, buyer_agent_id, product_id, buyer_power, seller_power, buyer_reservation_price, seller_reservation_price, current_strategy):
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
                    current_strategy=current_strategy
                )
                session.add(new_game)
                session.commit()
        except SQLAlchemyError as e:
            logging.error(f"Error storing game: {e}")


    def read_game(self, product_id):
        try:
            with self.Session() as session:
                return session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()
        except SQLAlchemyError as e:
            logging.error(f"Error reading game: {e}")


    def update_game_strategy(self, product_id, new_strategy):
        try:
            with self.Session() as session:
                game = session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()
                if game:
                    game.current_strategy = new_strategy
                    session.commit()
                    return game
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

        
# if __name__== "__main__":
    # Test
    # ds = DataService()
    # print(ds.read_buyer(name="Brandon Morrow").email)