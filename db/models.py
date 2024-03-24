from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)


class Shelf(Base):
    __tablename__ = 'shelves'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)

    status = relationship('Status', backref='orders')


class ProductOrder(Base):
    __tablename__ = 'product_orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship('Product', backref='product_orders')
    order = relationship('Order', backref='product_orders')

    __table_args__ = (
        UniqueConstraint('product_id', 'order_id'),
    )


class ShelfProduct(Base):
    __tablename__ = 'shelves_product'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    shelf_id = Column(Integer, ForeignKey('shelves.id'), nullable=False)
    is_main = Column(Boolean, nullable=False)

    product = relationship('Product', backref='shelf_products')
    shelf = relationship('Shelf', backref='shelf_products')

    __table_args__ = (
        UniqueConstraint('product_id', 'shelf_id'),
    )


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
