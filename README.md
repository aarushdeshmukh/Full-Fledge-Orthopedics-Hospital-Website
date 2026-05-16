# 🏥 Sonavane Hospital — Orthopedic Centre Web Application

A full-stack hospital appointment booking and management system built as a **Final Year Project**. The project simulates a real-world orthopedic hospital web application with a patient-facing booking system and a complete admin panel.

---

## 📌 Project Overview

The goal of this project was to build a real-world, production-level web application for a hospital. Patients can discover doctors, learn about services, and book appointments online. Hospital staff can manage everything through a dedicated admin dashboard — all built from scratch using Python Flask and SQLite.

---

## ✨ Features

### Patient Side
- **Home Page** — Hero section, featured doctors, services overview, testimonials, insurance info, and emergency contact
- **Doctor Listing** — Browse all available specialist doctors with qualifications, experience, and availability
- **Appointment Booking** — Logged-in patients can book appointments by selecting a doctor, date, and time slot
- **My Appointments** — View booking history with real-time status (pending / confirmed / cancelled)
- **Services Page** — Detailed list of all orthopedic services offered
- **About Page** — Hospital background, certifications, and facilities
- **User Authentication** — Register and login system with hashed passwords

### Admin Panel
- **Dashboard** — Stats for total appointments, pending, confirmed, and registered patients
- **Manage Appointments** — Confirm or cancel any appointment in real time
- **Manage Doctors** — Add new doctors or remove existing ones
- **Secure Admin Login** — Separate login route for hospital staff

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (via `sqlite3`) |
| Frontend | HTML5, CSS3 (custom), Vanilla JavaScript |
| Templating | Jinja2 |
| Auth | Werkzeug password hashing |
| Fonts | Google Fonts — Playfair Display, DM Sans |

---

## 📁 Project Structure

```
sonavane-hospital/
│
├── app.py                  # Main Flask application & all routes
├── sonavane.db             # SQLite database (auto-created on first run)
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── base.html           # Base layout with navbar & footer
│   ├── index.html          # Home page
│   ├── doctors.html        # Doctors listing
│   ├── book.html           # Appointment booking form
│   ├── my_appointments.html# Patient appointment history
│   ├── services.html       # Services page
│   ├── about.html          # About page
│   ├── login.html          # Patient login
│   ├── register.html       # Patient registration
│   ├── admin_login.html    # Admin login
│   ├── admin_dashboard.html# Admin control panel
│   └── skeleton.html       # Utility/skeleton page
│
└── static/
    ├── css/
    │   └── style.css       # All custom styles & CSS variables
    ├── js/
    │   └── main.js         # Scroll reveal, navbar, hamburger menu
    └── images/             # Doctor photos, hospital gallery images
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/aarushdeshmukh/sonavane-hospital.git
cd sonavane-hospital

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

The app will start at `http://127.0.0.1:5000`

The database and seed data (doctors + admin account) are created automatically on first run.

---

## 🔐 Default Credentials

### Admin Panel
- URL: `/admin/login`
- Username: `admin`
- Password: `admin123`

> ⚠️ Change the admin password before deploying to production.

---

## 🗄️ Database Schema

**users** — Registered patients (name, email, phone, age, gender, hashed password)

**doctors** — Doctor profiles (name, specialization, qualification, experience, availability, timing)

**appointments** — Bookings linking patients and doctors (date, time slot, problem, status)

**admins** — Admin credentials (username, hashed password)

---

## 📱 Pages & Routes

| Route | Description |
|---|---|
| `/` | Home page |
| `/doctors` | All doctors |
| `/book` | Book appointment (login required) |
| `/my-appointments` | Patient appointment history (login required) |
| `/services` | Services offered |
| `/about` | About the hospital |
| `/login` | Patient login |
| `/register` | New patient registration |
| `/logout` | Logout |
| `/admin/login` | Admin login |
| `/admin` | Admin dashboard |
| `/admin/logout` | Admin logout |

---

## 🚀 Deployment Notes

- Set a strong `app.secret_key` in `app.py` before going live
- Move the database to a persistent volume if deploying on a cloud server
- Serve static files via Nginx in production rather than Flask's built-in server
- Consider migrating from SQLite to PostgreSQL or MySQL for production workloads

---

## 👨‍💻 Developer

Developed by **Aarush Deshmukh**

- GitHub: [@aarushdeshmukh](https://github.com/aarushdeshmukh)

The entire project — backend architecture, database design, routing, frontend layout, and UI/UX — was built by me. Minor frontend styling assistance was taken from Claude AI; all core development, logic, and structure were done independently.

---

*© 2024 Aarush Deshmukh. Final Year Project.*
