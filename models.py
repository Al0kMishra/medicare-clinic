from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(100), nullable=False)
    dob          = Column(String(20),  nullable=True)
    gender       = Column(String(20),  nullable=True, default="Female")
    phone        = Column(String(30),  nullable=False)
    email        = Column(String(100), nullable=True, unique=True)
    blood_group  = Column(String(10),  nullable=True, default="O+")
    condition    = Column(String(200), nullable=True)
    allergies    = Column(String(200), nullable=True, default="None")
    history      = Column(Text,        nullable=True)
    last_visit   = Column(String(20),  nullable=True)
    password     = Column(String(256), nullable=True)


class Appointment(Base):
    __tablename__ = "appointments"

    id               = Column(Integer, primary_key=True, index=True)
    patient_id       = Column(Integer, nullable=True)
    patient_name     = Column(String(100), nullable=False)
    doctor           = Column(String(100), nullable=False)
    date             = Column(String(20),  nullable=False)
    time             = Column(String(20),  nullable=False)
    appt_type        = Column(String(100), nullable=False)
    status           = Column(String(20),  nullable=False, default="scheduled")
    notes            = Column(Text,        nullable=True)
    queue_number     = Column(Integer,     nullable=True)
    queue_status     = Column(String(30),  nullable=True, default="not_checked_in")
    checked_in_at    = Column(String(40),  nullable=True)
    called_at        = Column(String(40),  nullable=True)