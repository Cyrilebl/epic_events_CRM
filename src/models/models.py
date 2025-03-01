import re
from datetime import datetime
import bcrypt
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    name = Column(String, primary_key=True)

    __table_args__ = (
        CheckConstraint(
            "name IN ('manager', 'commercial', 'support')", name="role_name_check"
        ),
    )

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), index=True, nullable=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role_name = Column(String(10), ForeignKey("roles.name"), nullable=False)

    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="commercial")
    contracts = relationship("Contract", back_populates="commercial")
    events = relationship("Event", back_populates="support")

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.email} - {self.role_name})"

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    @staticmethod
    def validate_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password)

    def set_password(self, password):
        """Hash password"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)
        self.password_hash = hashed.decode("utf-8")

    def check_password(self, password):
        """Check if password match with hash password"""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), index=True, nullable=False)
    last_name = Column(String(100), index=True, nullable=False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    phone_number = Column(String(20), index=True, nullable=False)
    company_name = Column(String(255), index=True)
    information = Column(Text, nullable=False)
    creation_date = Column(
        Date, default=func.current_date(), index=True, nullable=False
    )
    last_update_date = Column(Date, onupdate=func.current_date())

    assigned_commercial = Column(Integer, ForeignKey("users.id"), nullable=False)

    commercial = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = r"^\+\d{2,3} \d{3} \d{3} \d{3}$"
        return re.match(pattern, phone_number)


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    total_price = Column(DECIMAL(10, 2), index=True, nullable=False)
    remaining_balance = Column(DECIMAL(10, 2), index=True, nullable=False)
    creation_date = Column(
        Date, default=func.current_date(), index=True, nullable=False
    )
    signature = Column(Boolean, index=True, default=False)

    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    assigned_commercial = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )

    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User", back_populates="contracts")
    event = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, index=True, nullable=False)
    end_date = Column(Date, index=True, nullable=False)

    street_number = Column(String(10), nullable=False)
    street_name = Column(String(255), nullable=False)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    contract_id = Column(
        Integer, ForeignKey("contracts.id"), index=True, nullable=False
    )
    assigned_support = Column(Integer, ForeignKey("users.id"), index=True)

    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="event")
    support = relationship("User", back_populates="events")

    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
