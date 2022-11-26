from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from database import Base, engine


class MassimoDuttiWomanProducts(Base):
    __tablename__ = "md_w_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("MassimoDuttiWomanPrices", back_populates="product")


class MassimoDuttiWomanPrices(Base):
    __tablename__ = "md_w_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(MassimoDuttiWomanProducts.id))

    product = relationship("MassimoDuttiWomanProducts", back_populates="prices")


class MassimoDuttiManProducts(Base):
    __tablename__ = "md_m_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("MassimoDuttiManPrices", back_populates="product")


class MassimoDuttiManPrices(Base):
    __tablename__ = "md_m_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(MassimoDuttiManProducts.id))

    product = relationship("MassimoDuttiManProducts", back_populates="prices")


class MassimoDuttiHighlightsProducts(Base):
    __tablename__ = "md_h_products"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    market = Column(String, nullable=False)
    url = Column(String, nullable=False)
    store_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    availability = Column(String)
    image = Column(String, nullable=False)

    prices = relationship("MassimoDuttiHighlightsPrices", back_populates="product")


class MassimoDuttiHighlightsPrices(Base):
    __tablename__ = "md_h_prices"
    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    price = Column(Integer, nullable=False)
    discount = Column(String)
    product_id = Column(Integer, ForeignKey(MassimoDuttiHighlightsProducts.id))

    product = relationship("MassimoDuttiHighlightsProducts", back_populates="prices")


Base.metadata.create_all(engine)
