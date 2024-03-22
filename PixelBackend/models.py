""" This file contains the models for the database. Each class represents a table in the database. """

from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    """This class represents the Users table in the database.

    Attributes:
    user_id: The primary key of the table. It is an integer.
    first_name: The first name of the user. It is a string.
    last_name: The last name of the user. It is a string.
    email: The email of the user. It is a string.
    password: The password of the user. It is a string.
    user_type: The type of the user. It is a string.
    phone: The phone number of the user. It is a string.
    address: The address of the user. It is a string.
    created_at: The timestamp of when the user was created. It is a timestamp.
    """

    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Product(Base):
    __tablename__ = "Products"

    prod_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    items_in_stock = Column(Integer, nullable=False)


class Category(Base):
    __tablename__ = "Categories"

    category_id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)


class Cart(Base):
    __tablename__ = "Carts"

    cart_id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# class CartItem(Base):
#     __tablename__ = "CartItems"

#     cart_item_id = Column(Integer, primary_key=True, index=True, nullable=False)
#     cart_id = Column(Integer, ForeignKey("Carts.cart_id"), nullable=False)
#     prod_id = Column(Integer, ForeignKey("Products.prod_id"), nullable=False)
#     prod_name = Column(String, ForeignKey("Products.name"), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     total_price = Column(Float, nullable=False)
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )


class Order(Base):
    __tablename__ = "Orders"

    order_id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("Users.user_id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    total_price = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    tax = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    discount_code = Column(String, nullable=False)


class OrderItem(Base):
    __tablename__ = "OrderItems"

    order_item_id = Column(Integer, primary_key=True, index=True, nullable=False)
    order_id = Column(
        Integer, ForeignKey("Orders.order_id", ondelete="CASCADE"), nullable=False
    )
    prod_id = Column(Integer, ForeignKey("Products.prod_id"), nullable=False)
    prod_name = Column(String, ForeignKey("Products.name"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class DiscountCode(Base):
    __tablename__ = "DiscountCodes"

    discount_code_id = Column(Integer, primary_key=True, index=True, nullable=False)
    code = Column(String, nullable=False)
    discount = Column(Float, nullable=False)
    active = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# class DiscountedProduct(Base):
#     __tablename__ = "DiscountedProducts"

#     discounted_product_id = Column(
#         Integer, primary_key=True, index=True, nullable=False
#     )
#     prod_id = Column(Integer, ForeignKey("Products.prod_id"), nullable=False)
#     discount_code_id = Column(
#         Integer, ForeignKey("DiscountCodes.discount_code_id"), nullable=False
#     )
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )