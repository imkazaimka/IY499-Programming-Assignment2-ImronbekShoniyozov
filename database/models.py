import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Enums for measure unit and supply type
class MeasureUnit(enum.Enum):
    kg = "kg"
    litre = "litre"
    pack = "pack"
    piece = "piece"

class SupplyType(enum.Enum):
    IN = "in"
    OUT = "out"

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    measure_unit = Column(Enum(MeasureUnit), nullable=False)
    manufacturer = Column(String(100))
    price = Column(Float, nullable=False)
    
    # Relationships
    stocks = relationship("Stock", back_populates="product", cascade="all, delete-orphan")
    supplies = relationship("Supply", back_populates="product", cascade="all, delete-orphan")
    promotions = relationship("Promotion", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', measure_unit='{self.measure_unit.value}', price={self.price})>"

class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    amount = Column(Float, nullable=False)
    
    # Relationship
    product = relationship("Product", back_populates="stocks")
    
    def __repr__(self):
        return f"<Stock(product_id={self.product_id}, amount={self.amount})>"

class Supply(Base):
    __tablename__ = 'supply'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    amount = Column(Float, nullable=False)
    in_or_out = Column(Enum(SupplyType), nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow)
    cashier = Column(String(100))
    
    # Relationships
    product = relationship("Product", back_populates="supplies")
    receipts = relationship("Receipt", back_populates="supply", cascade="all, delete-orphan")
    
    def __repr__(self):
        return (f"<Supply(product_id={self.product_id}, amount={self.amount}, "
                f"in_or_out='{self.in_or_out.value}', datetime='{self.datetime}', cashier='{self.cashier}')>")

class Promotion(Base):
    __tablename__ = 'promotion'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    datetime_start = Column(DateTime, nullable=False)
    datetime_end = Column(DateTime, nullable=False)
    discount = Column(Float, nullable=False)  # Discount percentage or value
    
    # Relationships
    product = relationship("Product", back_populates="promotions")
    receipts = relationship("Receipt", back_populates="promotion", cascade="all, delete-orphan")
    
    def __repr__(self):
        return (f"<Promotion(product_id={self.product_id}, discount={self.discount}, "
                f"start='{self.datetime_start}', end='{self.datetime_end}')>")

class Receipt(Base):
    __tablename__ = 'receipt'
    
    id = Column(Integer, primary_key=True)
    supply_id = Column(Integer, ForeignKey('supply.id'), nullable=False)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=True)
    
    # Relationships
    supply = relationship("Supply", back_populates="receipts")
    promotion = relationship("Promotion", back_populates="receipts")
    
    def __repr__(self):
        return f"<Receipt(supply_id={self.supply_id}, promotion_id={self.promotion_id})>"
