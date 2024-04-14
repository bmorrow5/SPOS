from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

"""This turns our database schema and tables into objects using SQLAlchemy ORM
"""

Base = declarative_base()

class SellerDatabase(Base):
    __tablename__ = 'sellers'
    __table_args__ = {'schema': 'spos'}
    seller_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

class BuyerAgentDatabase(Base):
    __tablename__ = 'buyer_agents'
    __table_args__ = {'schema': 'spos'}
    buyer_agent_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    employee_id = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

class ProductDatabase(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'spos'}
    product_id = Column(Integer, primary_key=True)
    buyer_agent_id = Column(Integer, ForeignKey('spos.buyer_agents.buyer_agent_id'))
    seller_id = Column(Integer, ForeignKey('spos.sellers.seller_id'))
    quantity = Column(Integer, nullable=False)
    max_price = Column(Float, nullable=False)
    date_needed_by = Column(TIMESTAMP, nullable=False)
    buyer = relationship("BuyerAgent")
    seller = relationship("Seller")

class GameDatabase(Base):
    __tablename__ = 'games'
    __table_args__ = {'schema': 'spos'}
    game_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('spos.sellers.seller_id'))
    buyer_agent_id = Column(Integer, ForeignKey('spos.buyer_agents.buyer_agent_id'))
    product_id = Column(Integer, ForeignKey('spos.products.product_id'))
    buyer_power = Column(Integer)
    seller_power = Column(Integer)
    buyer_reservation_price = Column(Float)
    seller_reservation_price = Column(Float)
    current_strategy = Column(String(255))
    buyer_agent = relationship("BuyerAgent")
    seller = relationship("Seller")
    product = relationship("Product")

class EmailLogDatabase(Base):
    __tablename__ = 'email_logs'
    __table_args__ = {'schema': 'spos'}
    email_log_id = Column(Integer, primary_key=True)
    sender_email = Column(String(255), nullable=False)
    receiver_email = Column(String(255), nullable=False)
    buyer_agent_id = Column(Integer, ForeignKey('spos.buyer_agents.buyer_agent_id'))
    seller_id = Column(Integer, ForeignKey('spos.sellers.seller_id'))
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    buyer_agent = relationship("BuyerAgent")
    seller = relationship("Seller")
