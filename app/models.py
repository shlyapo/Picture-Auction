import enum

from sqlalchemy import Integer, \
    Column, DateTime, ForeignKey, Text, Boolean, PrimaryKeyConstraint, ForeignKeyConstraint, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class MyEnum(enum.Enum):
    one = 'author'
    two = 'owner'
    three = 'actioneer'
    four = 'reviewer'


class User(Base):
    __tablename__ = 'users'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    login = Column(Text())
    password = Column(Text())
    name_user = Column(Text())
    surname = Column(Text())
    email = Column(Text())
    role = Column(Boolean(), default=False)
    admins = relationship("Admin", backref="user")
    owners = relationship("Owner", backref="user")
    authors = relationship("Author", backref="user")
    reviewers = relationship("Reviewer", backref="user")
    actioneers = relationship("Actioneer", backref="user")
    applications = relationship("Application", backref="user")
    logs = relationship("Log", backref="user")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Admin(Base):
    __tablename__ = 'administrators'
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    #user = relationship("User", backref="administrator")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='administrators_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Owner(Base):
    __tablename__ = 'owners'
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    work = Column(Text())
    #user = relationship("User", backref="owner")
    auctions = relationship("AuctionBuyer", backref="owner")
    pictures = relationship("Picture", backref="owner")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='owners_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Author(Base):
    __tablename__ = 'authors'
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    genre = Column(ARRAY(Text()))
    education = Column(Text())
    #user = relationship("User", backref="authors")
    pictures = relationship("Picture", backref="author")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='authors_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Actioneer(Base):
    __tablename__ = 'actioneers'
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    education = Column(Text())
    #user = relationship("User", backref="actioneer")
    auctions = relationship("Auction", backref="actioneer")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='actionners_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Reviewer(Base):
    __tablename__ = 'reviewers'
    extend_existing = True
    user_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    education = Column(Text())
    #user = relationship("User", backref="reviewer")
    reviews = relationship("Review", backref="reviewer")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='reviewers_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Log(Base):
    __tablename__ = 'logs'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    description = Column(Text())
    added = Column(DateTime())
    #user = relationship("User", backref="log")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='logs_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
    )


class Application(Base):
    __tablename__ = 'applications'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    admin_id = Column(Integer(), ForeignKey("administrators.user_id"))
    variant_request = Column(Enum(MyEnum))
    status = Column(Boolean())
    status_watch = Column(Boolean())
    #user = relationship("User", backref="application")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='applications_pkey'),
        ForeignKeyConstraint(['user_id'], ['users.id']),
        ForeignKeyConstraint(['admin_id'], ['administrators.user_id'])
    )


class ApplicationAuction(Base):
    __tablename__ = 'application_auction'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    auction_id = Column(Integer(), ForeignKey("auctions.id"))
    admin_id = Column(Integer(), ForeignKey("administrators.user_id"))
    status = Column(Boolean())
    __table_args__ = (
        PrimaryKeyConstraint('id', name='application_auction_pkey'),
        ForeignKeyConstraint(['auction_id'], ['auctions.id']),
        ForeignKeyConstraint(['admin_id'], ['administrators.user_id'])
    )


class Auction(Base):
    __tablename__ = 'auctions'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    actioneer_id = Column(Integer(), ForeignKey("actioneers.user_id"))
    date_of_action = Column(DateTime())
    status_apll = Column(Boolean())
    applications_auction = relationship("ApplicationAuction", backref="auction")
    pictures = relationship("AuctionPicture", backref="auction")
    owners = relationship("AuctionBuyer", backref="auction")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auctions_pkey'),
        ForeignKeyConstraint(['actioneer_id'], ['actioneers.user_id'])
    )


class Picture(Base):
    __tablename__ = 'pictures'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    auth_id = Column(Integer(), ForeignKey("authors.user_id"))
    owner_id = Column(Integer(), ForeignKey("owners.user_id"))
    name_pick = Column(Text())
    genre = Column(Text())
    cost_pick = Column(Integer())
    date_of_create = Column(DateTime())
    path_pick = Column(Text())
    auctions = relationship("AuctionPicture", backref="picture")
    reviews = relationship("Review", backref="picture")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pictures_pkey'),
        ForeignKeyConstraint(['auth_id'], ['authors.user_id']),
        ForeignKeyConstraint(['owner_id'], ['owners.user_id'])
    )


class Review(Base):
    __tablename__ = 'reviews'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    rev_id = Column(Integer(), ForeignKey("reviewers.user_id"))
    pick_id = Column(Integer(), ForeignKey("pictures.id"))
    message = Column(Text())
    date_of_review = Column(DateTime())
    __table_args__ = (
        PrimaryKeyConstraint('id', name='reviews_pkey'),
        ForeignKeyConstraint(['rev_id'], ['reviewers.user_id']),
        ForeignKeyConstraint(['pick_id'], ['pictures.id'])
    )


class AuctionBuyer(Base):
    __tablename__ = 'auction_buyers'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    auction_id = Column(Integer(), ForeignKey("auctions.id"))
    owner_id = Column(Integer(), ForeignKey("owners.user_id"))
    #owners = relationship("Owner", backref="auctionbuyer")
    #auctions = relationship("Auction", backref="auctionbuyer")
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auction_buyers_pkey'),
        ForeignKeyConstraint(['auction_id'], ['auctions.id']),
        ForeignKeyConstraint(['owner_id'], ['owners.user_id']),
    )


class AuctionPicture(Base):
    __tablename__ = 'auction_pictures'
    extend_existing = True
    id = Column(Integer(), primary_key=True)
    auction_id = Column(Integer(), ForeignKey("auctions.id"))
    pick_id = Column(Integer(), ForeignKey("pictures.id"))
    cost_on_auction = Column(Integer())
    own_id = Column(Integer(), ForeignKey("owners.user_id"))
    status_auc = Column(Boolean())
    __table_args__ = (
        PrimaryKeyConstraint('id', name='auction_buyers_pkey'),
        ForeignKeyConstraint(['auction_id'], ['auctions.id']),
        ForeignKeyConstraint(['own_id'], ['owners.id']),
        ForeignKeyConstraint(['pick_id'], ['pictures.id']),
    )

# enum + добавить relationship
enum

