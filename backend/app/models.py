from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date
from datetime import date


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class= Base)


# Allows multiple produce items to be linked to multiple shipping labels, and each shipping label to include multiple produce items
produce_shipping = Table(
    'produce_shipping', Base.metadata,
    Column('produce_id', Integer, ForeignKey('produce.id'), primary_key=True),
    Column('shippingLabel_id', Integer, ForeignKey('shippingLabel.id'), primary_key=True)
)

# Allows each shipping label to be associated with multiple contracts, and each contract to be linked to multiple shipping labels
shipping_contract = Table(
    'shipping_contract', Base.metadata,
    Column('shippingLabel_id', Integer, ForeignKey('shippingLabel.id'), primary_key=True),
    Column('contract_id', Integer, ForeignKey('contracts.id'), primary_key=True)
)

# Tracks what was grown, when it was picked, who was grown for, and which shipments it was included in
# Each produce item can be linked to multiple shipping labels, and each shipping label can include multiple produce items
class Produce(Base):
    __tablename__ = 'produce'
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.String(100), nullable=False)
    name: Mapped[str]= mapped_column(db.String(100), nullable=False)
    pick_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    contract_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('contracts.id'), nullable=True)
    contract = db.relationship('Contract', back_populates = 'produces')
    shipping_labels = db.relationship(
        'ShippingLabel',           # <-- Use class name, not table name
        secondary=produce_shipping,
        back_populates='produces',
    )

# Tracks customer orders, their details, and links them to both the produce grown and shipments sent to them
class Contract(Base):
    __tablename__ = 'contracts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable= False)
    email: Mapped[str] = mapped_column(db.String(100), nullable= False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable= False)
    produces = db.relationship('Produce', back_populates='contract', cascade="all, delete-orphan")
    shipping_labels = db.relationship(
        'ShippingLabel',           # <-- Use class name
        secondary=shipping_contract,
        back_populates='contracts',
    )
# Tracks each shipment, what produce it contains and which cutomer order it fulfills.
class ShippingLabel(Base):
    __tablename__ = 'shippingLabel'
    id: Mapped[int] = mapped_column(primary_key=True)
    produce_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('produce.id'))
    contract_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('contracts.id'))
    shipment_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    produces = db.relationship(
        'Produce',
        secondary=produce_shipping,
        back_populates='shipping_labels',
    )
    contracts = db.relationship(
        'Contract',
        secondary=shipping_contract,
        back_populates='shipping_labels',
    )


