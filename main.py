from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager

import models
import schemas
from database import engine, SessionLocal, get_db

from datetime import datetime as _dt

def today_str():
    return _dt.now().strftime("%Y-%m-%d")

def now_str():
    return _dt.now().strftime("%Y-%m-%d %H:%M:%S")



# ── Create tables ─────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="MediCare API",
    description="Clinic Management System — FastAPI + SQLite",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (allow all origins for local dev) ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Seed sample data on first run ─────────────────────────
def seed_data(db: Session):
    if db.query(models.Patient).count() > 0:
        return  # already seeded

    sample_patients = [
        models.Patient(name="Priya Sharma",  dob="1988-03-15", gender="Female", phone="+91 98765 43210", email="priya@email.com",  blood_group="B+",  condition="Hypertension",        allergies="Penicillin",   history="Hypertension since 2020. On Amlodipine 5mg daily.",                    last_visit="2026-03-10"),
        models.Patient(name="Arjun Mehta",   dob="1975-07-22", gender="Male",   phone="+91 87654 32109", email="arjun@email.com",  blood_group="O+",  condition="Diabetes Type 2",     allergies="None",         history="Type 2 DM since 2018. HbA1c checked quarterly.",                      last_visit="2026-03-15"),
        models.Patient(name="Sunita Rao",    dob="1992-11-08", gender="Female", phone="+91 76543 21098", email="sunita@email.com", blood_group="A+",  condition="Asthma",              allergies="Dust, Pollen", history="Mild asthma. Salbutamol inhaler as needed.",                           last_visit="2026-02-28"),
        models.Patient(name="Vikram Patel",  dob="1965-05-30", gender="Male",   phone="+91 65432 10987", email="vikram@email.com", blood_group="AB+", condition="Rheumatoid Arthritis",allergies="NSAIDs",       history="RA since 2015. On Methotrexate weekly.",                               last_visit="2026-03-18"),
        models.Patient(name="Meera Nair",    dob="2000-01-14", gender="Female", phone="+91 54321 09876", email="meera@email.com",  blood_group="O-",  condition="General Wellness",    allergies="None",         history="Healthy adult. Annual wellness checkups.",                             last_visit="2026-03-20"),
        models.Patient(name="Rohan Gupta",   dob="1983-09-25", gender="Male",   phone="+91 43210 98765", email="rohan@email.com",  blood_group="A-",  condition="Chronic Back Pain",   allergies="Latex",        history="L4-L5 disc bulge. Physiotherapy ongoing.",                            last_visit="2026-03-05"),
        models.Patient(name="Anjali Singh",  dob="1995-12-03", gender="Female", phone="+91 32109 87654", email="anjali@email.com", blood_group="B-",  condition="Migraine",            allergies="None",         history="Chronic migraines. On Topiramate prophylaxis.",                        last_visit="2026-03-12"),
        models.Patient(name="Deepak Verma",  dob="1970-04-18", gender="Male",   phone="+91 21098 76543", email="deepak@email.com", blood_group="AB-", condition="Hypothyroidism",      allergies="Shellfish",    history="Hypothyroidism. Levothyroxine 50mcg. TSH every 6 months.",            last_visit="2026-03-01"),
    ]
    db.add_all(sample_patients)
    db.flush()  # assigns IDs before commit

    pid = {p.name: p.id for p in sample_patients}

    sample_appts = [
        models.Appointment(patient_id=pid["Meera Nair"],    patient_name="Meera Nair",    doctor="Dr. Ayesha Khan", date="2026-03-20", time="09:00 AM", appt_type="General Checkup", status="completed",  notes="Annual wellness visit. All vitals normal."),
        models.Appointment(patient_id=pid["Priya Sharma"],  patient_name="Priya Sharma",  doctor="Dr. Rajiv Menon", date="2026-03-20", time="10:30 AM", appt_type="Follow-up",        status="completed",  notes="BP 130/85. Adjusted dosage."),
        models.Appointment(patient_id=pid["Arjun Mehta"],   patient_name="Arjun Mehta",   doctor="Dr. Ayesha Khan", date="2026-03-20", time="11:00 AM", appt_type="Follow-up",        status="scheduled",  notes="HbA1c review. Bring latest lab reports."),
        models.Appointment(patient_id=pid["Vikram Patel"],  patient_name="Vikram Patel",  doctor="Dr. Suresh Iyer", date="2026-03-20", time="02:00 PM", appt_type="Consultation",     status="scheduled",  notes="Joint pain assessment. Consider physio referral."),
        models.Appointment(patient_id=pid["Anjali Singh"],  patient_name="Anjali Singh",  doctor="Dr. Rajiv Menon", date="2026-03-21", time="09:30 AM", appt_type="Follow-up",        status="scheduled",  notes="Migraine treatment review."),
        models.Appointment(patient_id=pid["Sunita Rao"],    patient_name="Sunita Rao",    doctor="Dr. Ayesha Khan", date="2026-03-22", time="11:30 AM", appt_type="Check-up",         status="scheduled",  notes="Pulmonary function test results."),
        models.Appointment(patient_id=pid["Rohan Gupta"],   patient_name="Rohan Gupta",   doctor="Dr. Suresh Iyer", date="2026-03-19", time="03:00 PM", appt_type="Physiotherapy",    status="completed",  notes="Session 4. Improving range of motion."),
        models.Appointment(patient_id=pid["Deepak Verma"],  patient_name="Deepak Verma",  doctor="Dr. Rajiv Menon", date="2026-03-18", time="10:00 AM", appt_type="Lab Review",       status="completed",  notes="TSH 3.2 — within range. Continue dosage."),
        models.Appointment(patient_id=pid["Priya Sharma"],  patient_name="Priya Sharma",  doctor="Dr. Ayesha Khan", date="2026-03-25", time="09:00 AM", appt_type="Follow-up",        status="scheduled",  notes="Monthly BP monitoring."),
        models.Appointment(patient_id=pid["Arjun Mehta"],   patient_name="Arjun Mehta",   doctor="Dr. Rajiv Menon", date="2026-03-15", time="11:00 AM", appt_type="Lab Review",       status="cancelled",  notes="Patient cancelled — travel."),
    ]
    db.add_all(sample_appts)
    db.commit()
    print("✅  Database seeded with sample data.")



# ══════════════════════════════════════════════════════════
#  PATIENT ROUTES
# ══════════════════════════════════════════════════════════

@app.get("/patients", response_model=List[schemas.PatientOut], tags=["Patients"])
def list_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).order_by(models.Patient.name).all()


@app.get("/patients/{patient_id}", response_model=schemas.PatientOut, tags=["Patients"])
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p


@app.post("/patients", response_model=schemas.PatientOut, status_code=201, tags=["Patients"])
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    p = models.Patient(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@app.put("/patients/{patient_id}", response_model=schemas.PatientOut, tags=["Patients"])
def update_patient(patient_id: int, payload: schemas.PatientUpdate, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    db.commit()
    db.refresh(p)
    return p


@app.delete("/patients/{patient_id}", status_code=204, tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    # Also remove their appointments
    db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).delete()
    db.delete(p)
    db.commit()


# ══════════════════════════════════════════════════════════
#  APPOINTMENT ROUTES
# ══════════════════════════════════════════════════════════

@app.get("/appointments", response_model=List[schemas.AppointmentOut], tags=["Appointments"])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).order_by(models.Appointment.date, models.Appointment.time).all()



@app.get("/appointments/patient/{patient_id}", response_model=List[schemas.AppointmentOut], tags=["Appointments"])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    """Get all appointments for a specific patient (by id OR name match)."""
    # First get the patient name for fallback matching
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appts = db.query(models.Appointment).filter(
        (models.Appointment.patient_id == patient_id) |
        (models.Appointment.patient_name == patient.name)
    ).order_by(models.Appointment.date.desc(), models.Appointment.time.desc()).all()
    return appts

@app.post("/appointments", response_model=schemas.AppointmentOut, status_code=201, tags=["Appointments"])
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    a = models.Appointment(**payload.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@app.patch("/appointments/{appt_id}/status", response_model=schemas.AppointmentOut, tags=["Appointments"])
def update_appointment_status(appt_id: int, payload: schemas.StatusUpdate, db: Session = Depends(get_db)):
    valid = {"scheduled", "completed", "cancelled"}
    if payload.status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    a = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    a.status = payload.status
    db.commit()
    db.refresh(a)
    return a


@app.delete("/appointments/{appt_id}", status_code=204, tags=["Appointments"])
def delete_appointment(appt_id: int, db: Session = Depends(get_db)):
    a = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(a)
    db.commit()


# ══════════════════════════════════════════════════════════
#  PATIENT PORTAL
# ══════════════════════════════════════════════════════════

@app.post("/portal/book", response_model=schemas.AppointmentOut, status_code=201, tags=["Portal"])
def portal_book(payload: schemas.PortalBooking, db: Session = Depends(get_db)):
    a = models.Appointment(
        patient_id=None,
        patient_name=payload.name,
        doctor="Dr. Ayesha Khan",
        date=payload.date,
        time=payload.time,
        appt_type=payload.service,
        status="scheduled",
        notes=payload.notes,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


# ══════════════════════════════════════════════════════════
#  DASHBOARD STATS
# ══════════════════════════════════════════════════════════

@app.get("/stats", tags=["Dashboard"])
def get_stats(db: Session = Depends(get_db)):
    today     = today_str()
    week_end  = (_dt.now() + __import__("datetime").timedelta(days=7)).strftime("%Y-%m-%d")
    month     = _dt.now().strftime("%Y-%m")

    total_patients  = db.query(models.Patient).count()
    today_appts     = db.query(models.Appointment).filter(models.Appointment.date == today).count()
    week_appts      = db.query(models.Appointment).filter(
                        models.Appointment.date >= today,
                        models.Appointment.date <= week_end,
                        models.Appointment.status != "cancelled"
                      ).count()
    new_month       = db.query(models.Patient).filter(
                        models.Patient.last_visit.like(f"{month}%")
                      ).count()

    return {
        "total_patients": total_patients,
        "today_appointments": today_appts,
        "week_appointments": week_appts,
        "new_this_month": new_month,
    }


@app.get("/queue/patient/{patient_id}", tags=["Queue"])
def get_patient_queue_status(patient_id: int, db: Session = Depends(get_db)):
    """Get queue status for a patient — today's appointment or next upcoming one."""
    today = today_str()

    # Resolve patient name first (simple separate query — avoids subquery issues)
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    patient_name = patient.name if patient else None

    # Find next appointment (today first, then upcoming) by patient_id or name
    appt = None
    if patient_name:
        appt = (
            db.query(models.Appointment)
            .filter(
                models.Appointment.status != "cancelled",
                models.Appointment.date >= today,
                (
                    (models.Appointment.patient_id == patient_id) |
                    (models.Appointment.patient_name == patient_name)
                )
            )
            .order_by(models.Appointment.date, models.Appointment.time)
            .first()
        )

    if not appt:
        return {"has_appointment": False, "mode": None}

    is_today = appt.date == today

    # Count people ahead in today's queue
    ahead = 0
    est_wait = 0
    now_serving_token = None
    now_serving_name = None

    if is_today:
        waiting_list = (
            db.query(models.Appointment)
            .filter(
                models.Appointment.date == today,
                models.Appointment.queue_status == "waiting",
                models.Appointment.status != "cancelled"
            ).all()
        )
        serving = db.query(models.Appointment).filter(
            models.Appointment.date == today,
            models.Appointment.queue_status == "serving"
        ).first()

        if appt.queue_status == "waiting":
            ahead = sum(1 for a in waiting_list if (a.queue_number or 0) < (appt.queue_number or 0))
            est_wait = ahead * 15

        now_serving_token = serving.queue_number if serving else None
        now_serving_name  = serving.patient_name if serving else None

    return {
        "has_appointment":    True,
        "mode":               "today" if is_today else "upcoming",
        "appt_id":            appt.id,
        "queue_token":        appt.queue_number,
        "queue_status":       appt.queue_status or "waiting",
        "scheduled_time":     appt.time,
        "date":               appt.date,
        "doctor":             appt.doctor,
        "appt_type":          appt.appt_type,
        "ahead":              ahead,
        "est_wait_mins":      est_wait,
        "now_serving_token":  now_serving_token,
        "now_serving_name":   now_serving_name,
    }


# ══════════════════════════════════════════════════════════
#  AUTH ROUTES
# ══════════════════════════════════════════════════════════
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@app.post("/auth/register", response_model=schemas.AuthOut, status_code=201, tags=["Auth"])
def register_patient(payload: schemas.PatientRegister, db: Session = Depends(get_db)):
    # Check duplicate email
    existing = db.query(models.Patient).filter(models.Patient.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    # Check duplicate phone
    existing_phone = db.query(models.Patient).filter(models.Patient.phone == payload.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="An account with this phone number already exists.")

    patient = models.Patient(
        name        = payload.name,
        email       = payload.email,
        phone       = payload.phone,
        dob         = payload.dob,
        gender      = payload.gender,
        blood_group = payload.blood_group,
        password    = hash_password(payload.password),
        allergies   = "None",
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@app.post("/auth/login", response_model=schemas.AuthOut, tags=["Auth"])
def login_patient(payload: schemas.PatientLogin, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.email == payload.email).first()
    if not patient:
        raise HTTPException(status_code=401, detail="No account found with this email.")
    if not patient.password:
        raise HTTPException(status_code=401, detail="This account was added by clinic staff. Please contact the clinic to set your password.")
    if patient.password != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Incorrect password.")
    return patient


# ══════════════════════════════════════════════════════════
#  QUEUE ROUTES
# ══════════════════════════════════════════════════════════

@app.get("/queue/today", tags=["Queue"])
def get_today_queue(db: Session = Depends(get_db)):
    """All of today's non-cancelled appointments, ordered by queue number then scheduled time."""
    today = today_str()
    appts = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.date == today,
            models.Appointment.status != "cancelled"
        )
        .order_by(
            models.Appointment.queue_number.nullslast(),
            models.Appointment.time
        )
        .all()
    )
    # Build rich queue objects
    waiting = [a for a in appts if a.queue_status == "waiting"]
    in_consultation = next((a for a in appts if a.queue_status == "in_consultation"), None)

    result = []
    for a in appts:
        position = None
        eta_mins = None
        if a.queue_status == "waiting":
            position = waiting.index(a) + 1
            ahead    = position - 1
            # Each slot ~10 mins; if someone is in consultation add remaining time
            eta_mins = ahead * 10
            if in_consultation:
                eta_mins += 5  # assume ~5 mins left for current
        result.append({
            "id":            a.id,
            "patient_id":    a.patient_id,
            "patient_name":  a.patient_name,
            "doctor":        a.doctor,
            "scheduled_time":a.time,
            "appt_type":     a.appt_type,
            "status":        a.status,
            "queue_number":  a.queue_number,
            "queue_status":  a.queue_status or "not_checked_in",
            "checked_in_at": a.checked_in_at,
            "called_at":     a.called_at,
            "queue_position":position,
            "eta_mins":      eta_mins,
            "notes":         a.notes,
        })
    return result


@app.post("/queue/checkin/{appt_id}", tags=["Queue"])
def checkin(appt_id: int, db: Session = Depends(get_db)):
    """Patient or admin checks a patient into today's queue."""
    a = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if a.queue_status not in (None, "not_checked_in"):
        raise HTTPException(status_code=400, detail="Already checked in")

    # Assign next queue number for today
    today = today_str()
    max_q = db.query(models.Appointment).filter(
        models.Appointment.date == today,
        models.Appointment.queue_number != None
    ).count()

    a.queue_number  = max_q + 1
    a.queue_status  = "waiting"
    a.checked_in_at = now_str()
    db.commit()
    db.refresh(a)
    return {"queue_number": a.queue_number, "queue_status": a.queue_status}


@app.post("/queue/call-next", tags=["Queue"])
def call_next(db: Session = Depends(get_db)):
    """Admin calls the next waiting patient."""
    today = today_str()
    # Finish anyone currently in consultation
    current = db.query(models.Appointment).filter(
        models.Appointment.date == today,
        models.Appointment.queue_status == "in_consultation"
    ).first()
    if current:
        current.queue_status = "done"
        current.status = "completed"

    # Get next waiting
    nxt = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.date == today,
            models.Appointment.queue_status == "waiting"
        )
        .order_by(models.Appointment.queue_number)
        .first()
    )
    if not nxt:
        db.commit()
        return {"message": "No more patients in queue"}

    nxt.queue_status = "in_consultation"
    nxt.called_at    = now_str()
    db.commit()
    db.refresh(nxt)
    return {
        "called": nxt.patient_name,
        "queue_number": nxt.queue_number,
        "doctor": nxt.doctor
    }


@app.patch("/queue/{appt_id}/status", tags=["Queue"])
def update_queue_status(appt_id: int, payload: schemas.StatusUpdate, db: Session = Depends(get_db)):
    """Manually set queue status for an appointment."""
    valid = {"not_checked_in", "waiting", "called", "in_consultation", "done", "skipped"}
    if payload.status not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    a = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    a.queue_status = payload.status
    if payload.status == "done":
        a.status = "completed"
    db.commit()
    db.refresh(a)
    return {"id": a.id, "queue_status": a.queue_status}


@app.get("/queue/position/{appt_id}", tags=["Queue"])
def my_queue_position(appt_id: int, db: Session = Depends(get_db)):
    """Patient polls this to see their current queue position and ETA."""
    today = today_str()
    a = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")

    waiting = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.date == today,
            models.Appointment.queue_status == "waiting"
        )
        .order_by(models.Appointment.queue_number)
        .all()
    )
    in_consultation = db.query(models.Appointment).filter(
        models.Appointment.date == today,
        models.Appointment.queue_status == "in_consultation"
    ).first()

    position = None
    eta_mins = None
    if a.queue_status == "waiting":
        ids = [w.id for w in waiting]
        if a.id in ids:
            position = ids.index(a.id) + 1
            ahead    = position - 1
            eta_mins = ahead * 10 + (5 if in_consultation else 0)
    elif a.queue_status == "in_consultation":
        position = 0  # currently being seen

    return {
        "appt_id":       a.id,
        "patient_name":  a.patient_name,
        "queue_number":  a.queue_number,
        "queue_status":  a.queue_status or "not_checked_in",
        "scheduled_time":a.time,
        "doctor":        a.doctor,
        "queue_position":position,
        "eta_mins":      eta_mins,
        "in_consultation_now": in_consultation.patient_name if in_consultation else None,
    }
