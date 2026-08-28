# 🏥 AyurX - Hospital Management System

AyurX is a full-stack Hospital Management System designed to simplify hospital operations and improve the patient experience.

The system provides a platform for managing hospitals, doctors, patients, appointments, and patient profiles. Patients can browse hospitals, view available doctors, book appointments, and track their appointment status.

---

## 🚀 Features

### 👤 Patient

- Patient registration and login
- View available hospitals
- View doctors
- Book appointments
- View appointment status
- Edit patient profile
- Manage personal information

### 👨‍⚕️ Doctor

- Doctor management
- View assigned appointments
- Manage patient-related appointment information
- Access doctor information

### 🏥 Hospital

- Hospital management
- Manage hospital information
- Manage doctors associated with hospitals
- Manage appointments

### 📅 Appointment Management

- Online appointment booking
- Patient appointment requests
- Appointment status tracking
- Approved / pending appointment status
- Doctor and hospital association

### 🔐 Authentication

- User registration
- User login
- User logout
- Role-based access to different sections of the system

---

## 🛠️ Technologies Used

### Frontend

- HTML
- Tailwind CSS
- JavaScript

### Backend

- Python
- Django
- Django REST Framework

### Database

- PostgreSQL

### Deployment

- Render

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │      Users       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Frontend      │
                    │ HTML + Tailwind  │
                    │   + JavaScript   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Django Backend   │
                    │    + DRF         │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌─────────────┐ ┌────────────┐
       │ PostgreSQL │ │ Appointment  │ │   Users    │
       │  Database  │ │ Management   │ │ Management │
       └────────────┘ └─────────────┘ └────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Hospital / Doctor│
                    │    / Patient     │
                    └──────────────────┘
