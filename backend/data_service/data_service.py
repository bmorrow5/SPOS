from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import SellerDatabase, BuyerAgentDatabase, ProductDatabase, GameDatabase, EmailLogDatabase



class DataService():
    """This class serves as the data service for the application, and will perform CRUD operations on all database tables
    """

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:spos123@localhost:5432/default_company')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


    ############## Seller CRUD ##############
    def create_seller(self, name, email):
        with self.Session() as session:
            new_seller = SellerDatabase(name=name, email=email)
            session.add(new_seller)
            session.commit()

    def read_seller(self, name=None, email=None):
        with self.Session() as session:
            if name:
                return session.query(SellerDatabase).filter_by(name=name).one_or_none()
            elif email:
                return session.query(SellerDatabase).filter_by(email=email).one_or_none()
            else:
                return None

    def update_seller_email(self, name=None, email=None):
        with self.Session() as session:
            seller =  session.query(SellerDatabase).filter_by(name=name).one_or_none()
            if email:
                seller.email = email
            session.commit()
            return seller

    def delete_seller(self, name=None, email=None):
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
        
    ############## Buyer CRUD ##############
    def create_buyer(self, name, employee_id, email, password):
        with self.Session() as session:
            new_buyer = BuyerAgentDatabase(name=name, employee_id = employee_id, email=email, password=password)
            session.add(new_buyer)
            session.commit()

    def read_buyer(self, name=None, employee_id=None, email=None, password=None):
        """Can take any buyer identifier and will pull their information
        """
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

    def update_buyer(self, name=None, employee_id=None, email=None, password=None):
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

    def delete_buyer(self, buyer_id):
        with self.Session() as session:
            buyer = session.query(BuyerAgentDatabase).filter_by(buyer_id=buyer_id).one_or_none()
            if buyer:
                session.delete(buyer)
                session.commit()
                return True
            return False
        
    ############## Product CRUD ##############
    def create_product(self, buyer_agent_id, seller_id, quantity, max_price, date_needed_by):
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

    def read_product(self, buyer_agent_id=None, seller_id=None):
        with self.Session() as session:
            if buyer_agent_id and seller_id:
                return session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id, seller_id=seller_id).all()
            elif buyer_agent_id:
                return session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id).all()
            elif seller_id:
                return session.query(ProductDatabase).filter_by(seller_id=seller_id).all()

    def update_product(self, buyer_agent_id, seller_id, new_quantity=None, new_max_price=None, new_date_needed_by=None):
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

    def delete_product(self, buyer_agent_id, seller_id):
        with self.Session() as session:
            products = session.query(ProductDatabase).filter_by(buyer_agent_id=buyer_agent_id, seller_id=seller_id).all()
            for product in products:
                session.delete(product)
            session.commit()
            return True


    ############## Game CRUD ##############
    def create_game(self, seller_id, buyer_agent_id, product_id, buyer_power, seller_power, buyer_reservation_price, seller_reservation_price, current_strategy):
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

    def read_game(self, product_id):
        with self.Session() as session:
            return session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()

    def update_game_strategy(self, product_id, new_strategy):
        with self.Session() as session:
            game = session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()
            if game:
                game.current_strategy = new_strategy
                session.commit()
                return game

    def delete_game(self, product_id):
        with self.Session() as session:
            game = session.query(GameDatabase).filter_by(product_id=product_id).one_or_none()
            if game:
                session.delete(game)
                session.commit()
                return True
            
    ############## EmailLog CRUD ##############
    def create_email_log(self, sender_email, receiver_email, subject, body, buyer_agent_id=None, seller_id=None):
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

    def read_email_logs_by_sender(self, sender_email):
        with self.Session() as session:
            return session.query(EmailLogDatabase).filter_by(sender_email=sender_email).all()
        
    def read_email_logs_by_receiver(self, receiver_email):
        with self.Session() as session:
            return session.query(EmailLogDatabase).filter_by(receiver_email=receiver_email).all()

    def update_email_log(self, email_log_id, new_subject=None, new_body=None):
        with self.Session() as session:
            email_log = session.query(EmailLogDatabase).filter_by(email_log_id=email_log_id).one_or_none()
            if email_log:
                if new_subject:
                    email_log.subject = new_subject
                if new_body:
                    email_log.body = new_body
                session.commit()
                return email_log

    def delete_email_log(self, email_log_id):
        with self.Session() as session:
            email_log = session.query(EmailLogDatabase).filter_by(email_log_id=email_log_id).one_or_none()
            if email_log:
                session.delete(email_log)
                session.commit()
                return True
            return False

        
