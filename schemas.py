from pydantic import BaseModel
from typing import Optional


# ── Patient ──────────────────────────────────────────────
class PatientCreate(BaseModel):
    name:        str
    phone:       str
    dob:         Optional[str] = None
    gender:      Optional[str] = "Female"
    email:       Optional[str] = None
    blood_group: Optional[str] = "O+"
    condition:   Optional[str] = None
    allergies:   Optional[str] = "None"
    history:     Optional[str] = None
    last_visit:  Optional[str] = None


class PatientUpdate(BaseModel):
    name:        Optional[str] = None
    phone:       Optional[str] = None
    dob:         Optional[str] = None
    gender:      Optional[str] = None
    email:       Optional[str] = None
    blood_group: Optional[str] = None
    condition:   Optional[str] = None
    allergies:   Optional[str] = None
    history:     Optional[str] = None
    last_visit:  Optional[str] = None


class PatientOut(BaseModel):
    id:          int
    name:        str
    phone:       str
    dob:         Optional[str]
    gender:      Optional[str]
    email:       Optional[str]
    blood_group: Optional[str]
    condition:   Optional[str]
    allergies:   Optional[str]
    history:     Optional[str]
    last_visit:  Optional[str]

    class Config:
        from_attributes = True


# ── Appointment ───────────────────────────────────────────
class AppointmentCreate(BaseModel):
    patient_id:   Optional[int]  = None
    patient_name: str
    doctor:       str
    date:         str
    time:         str
    appt_type:    str
    status:       Optional[str]  = "scheduled"
    notes:        Optional[str]  = None


class AppointmentOut(BaseModel):
    id:           int
    patient_id:   Optional[int]
    patient_name: str
    doctor:       str
    date:         str
    time:         str
    appt_type:    str
    status:       str
    notes:        Optional[str]

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str


# ── Portal booking ────────────────────────────────────────
class PortalBooking(BaseModel):
    name:    str
    phone:   str
    email:   Optional[str] = None
    service: str
    date:    str
    time:    str
    notes:   Optional[str] = None


# ── Auth ──────────────────────────────────────────────────
class PatientRegister(BaseModel):
    name:        str
    email:       str
    phone:       str
    password:    str
    dob:         Optional[str] = None
    gender:      Optional[str] = "Female"
    blood_group: Optional[str] = "O+"


class PatientLogin(BaseModel):
    email:    str
    password: str


class AuthOut(BaseModel):
    id:          int
    name:        str
    email:       Optional[str]
    phone:       str
    dob:         Optional[str]
    gender:      Optional[str]
    blood_group: Optional[str]
    condition:   Optional[str]
    allergies:   Optional[str]
    history:     Optional[str]
    last_visit:  Optional[str]

    class Config:
        from_attributes = True