from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    membership_id = Column(Integer, ForeignKey('memberships.id'))
    
    membership = relationship('Membership', back_populates='members')
    trainers = relationship('Trainer', secondary='member_trainers', back_populates='members')
    transactions = relationship("Transaction", back_populates="member")

class Membership(Base):
    __tablename__ = 'memberships'
    
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # Basic, Standard, Premium
    price = Column(Integer, nullable=False)
    
    members = relationship('Member', back_populates='membership')

class Trainer(Base):
    __tablename__ = 'trainers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    
    members = relationship('Member', secondary='member_trainers', back_populates='trainers')

class MemberTrainer(Base):
    __tablename__ = 'member_trainers'
    
    member_id = Column(Integer, ForeignKey('members.id'), primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), primary_key=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    member = relationship("Member", back_populates="transactions")

engine = create_engine('sqlite:///gym.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
