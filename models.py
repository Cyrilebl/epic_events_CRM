from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Date,
    Boolean,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    name = Column(String, primary_key=True)

    __table_args__ = CheckConstraint(
        "name IN ('manager', 'commercial', 'support')", name="role_name_check"
    )

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, index=True)

    role_name = Column(Integer, ForeignKey("roles.name"), nullable=False)

    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="commercial")
    contracts = relationship("Contract", back_populates="commercial")
    events = relationship("Event", back_populates="support")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String, index=True)
    company_name = Column(String, index=True)
    information = Column(String)
    creation_date = Column(Date, index=True)
    last_update_date = Column(Date)

    assigned_commercial = Column(Integer, ForeignKey("users.id"))

    commercial = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="clients")
    events = relationship("Event", back_populates="clients")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    total_price = Column(Float, index=True)
    remaining_balance = Column(Float, index=True)
    creation_date = Column(Date, index=True)
    signature = Column(Boolean, index=True, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"))
    assigned_commercial = Column(Integer, ForeignKey("users.id"))

    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User", back_populates="contracts")
    event = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)

    client_id = Column(Integer, ForeignKey("clients.id"))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    assigned_support = Column(Integer, ForeignKey("users.id"))

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="event")
    support = relationship("User", back_populates="events")
