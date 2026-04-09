# 🏥 MediCare — Clinic Management System

A full-stack clinic management web app built with **FastAPI** (Python) on the backend and plain **HTML/CSS/JS** on the frontend. Designed for small clinics to manage patients, appointments, and a live queue system.

---

## 📁 Project Structure

```
medicare-clinic/
├── main.py          # FastAPI app — all API routes
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Database engine and session setup
├── medicare.db      # SQLite database (auto-created on first run)
├── index.html       # Admin dashboard
├── login.html       # Login & registration page
├── patient.html     # Patient portal — health records & queue status
└── queue.html       # Live queue management board
```

---

## ✨ Features

### 👨‍⚕️ Admin Panel
- View, add, edit, and delete patients
- Schedule and manage appointments
- Update appointment statuses (scheduled / completed / cancelled)
- Live queue management board with auto-refresh every 10 seconds
- Check patients in, call next patient, skip patients
- Dashboard stats — total patients, today's appointments, weekly count

### 🧑‍💼 Patient Portal
- Patient registration and login
- View personal health records (blood group, allergies, medical history)
- Book appointments through the portal
- Track live queue position and estimated wait time

### 📋 Queue System
- Patients check in on arrival and receive a queue number
- Admin calls next patient with one click
- Real-time position and ETA updates
- Statuses: Not Checked In → Waiting → In Consultation → Done

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Fonts | Google Fonts — Nunito, Fraunces |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Al0kMishra/medicare-clinic.git
cd medicare-clinic
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy
```

**4. Start the server**
```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`

**5. Open the frontend**

Simply open any `.html` file in your browser. All pages point to `http://localhost:8000` automatically.

> 💡 Tip: Use the **Live Server** extension in VS Code for a better experience.

---

## 📡 API Endpoints

### Patients
| Method | Endpoint | Description |
|---|---|---|
| GET | `/patients` | List all patients |
| GET | `/patients/{id}` | Get a patient by ID |
| POST | `/patients` | Create a new patient |
| PUT | `/patients/{id}` | Update a patient |
| DELETE | `/patients/{id}` | Delete a patient |

### Appointments
| Method | Endpoint | Description |
|---|---|---|
| GET | `/appointments` | List all appointments |
| GET | `/appointments/patient/{id}` | Get appointments by patient |
| POST | `/appointments` | Create an appointment |
| PATCH | `/appointments/{id}/status` | Update appointment status |
| DELETE | `/appointments/{id}` | Delete an appointment |

### Queue
| Method | Endpoint | Description |
|---|---|---|
| GET | `/queue/today` | Get today's full queue |
| POST | `/queue/checkin/{id}` | Check a patient into the queue |
| POST | `/queue/call-next` | Call the next waiting patient |
| PATCH | `/queue/{id}/status` | Manually update queue status |
| GET | `/queue/position/{id}` | Get a patient's queue position |
| GET | `/queue/patient/{id}` | Get queue status for a patient |

### Auth & Portal
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new patient account |
| POST | `/auth/login` | Patient login |
| POST | `/portal/book` | Book an appointment via patient portal |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/stats` | Get dashboard stats |

> 📖 Full interactive API docs available at `http://127.0.0.1:8000/docs` after starting the server.

---

## 🗃️ Sample Data

The app automatically seeds the database with **8 sample patients** and **10 sample appointments** on the first run, so you can explore all features immediately without any setup.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
