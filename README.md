# 🎓 CampusHire — Placement Management Portal

> A full-stack campus placement management system that connects **students, companies, and administrators** through a centralized platform for managing placement drives, applications, eligibility, and recruitment workflows.

[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js-42b883?logo=vue.js\&logoColor=white)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![Redis](https://img.shields.io/badge/Cache-Redis-DC382D?logo=redis\&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Tasks-Celery-37814A?logo=celery\&logoColor=white)](https://docs.celeryq.dev/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**CampusHire** is a full-stack placement management platform designed to simplify and centralize the campus recruitment process.

The system provides separate workflows for:

* 👨‍🎓 **Students**
* 🏢 **Companies**
* 👨‍💼 **Administrators**

Students can maintain their profiles, view eligible placement drives, and apply for opportunities. Companies can register, create placement drives, define eligibility criteria, and manage applications. Administrators control company approvals, placement drives, users, and overall placement activity.

The backend exposes REST APIs documented using **OpenAPI**, while the frontend is built using **Vue 3 and Vite**.

---

## ✨ Features

### 👨‍🎓 Student Module

* Student registration and login
* JWT-based authentication
* Student profile management
* Academic information management
* CGPA management
* Branch and graduation-year information
* Resume link management
* Browse active placement drives
* View complete placement-drive details
* Check eligibility requirements
* Apply for placement drives
* Track application status
* View participating/approved companies
* Blocked-student protection

Students can only apply when their profile contains the required information and they satisfy the placement-drive eligibility requirements.

---

### 🏢 Company Module

Companies can:

* Register their organization
* Maintain company information
* Provide HR contact details
* Wait for administrator approval
* Create placement drives
* Define:

  * Job title
  * Job description
  * Eligible branches
  * Minimum CGPA
  * Eligible graduation year
  * Application deadline
* View placement drives
* Monitor applications
* View student information
* Manage company profile

A company must be approved by an administrator before it can create a placement drive.

---

### 👨‍💼 Admin Module

Administrators can:

* Approve companies
* Reject companies
* Approve placement drives
* Block/reject placement drives
* View companies
* Manage students
* Manage placement activity
* Monitor applications
* Access placement statistics
* Control platform-level workflows

The backend protects administrative endpoints using role-based authorization.

---

## 🔐 Authentication & Authorization

CampusHire uses **JWT (JSON Web Tokens)** for authentication.

The login endpoint accepts:

* Email
* Password
* Role

Supported roles:

```text
student
company
admin
```

After successful authentication, the server returns a JWT containing the user's role, which is then used to protect role-specific API endpoints.

### Authorization Flow

```text
                    ┌──────────────┐
                    │    Login     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ JWT Token    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐   ┌─────────┐   ┌────────┐
         │ Student│   │ Company │   │ Admin  │
         └────────┘   └─────────┘   └────────┘
```

---

## 🏗️ Architecture

CampusHire follows a separated frontend/backend architecture.

```text
┌──────────────────────────────────────────────┐
│                  Frontend                    │
│                                              │
│              Vue 3 + Vite                   │
│          Vue Router + Axios                  │
└──────────────────────┬───────────────────────┘
                       │
                       │ REST API / JSON
                       ▼
┌──────────────────────────────────────────────┐
│                  Backend                     │
│                                              │
│                 Flask                       │
│          JWT Authentication                 │
│          Role-based Authorization            │
└───────────────┬───────────────┬──────────────┘
                │               │
                ▼               ▼
       ┌────────────────┐   ┌───────────────┐
       │    SQLite      │   │     Redis     │
       │   Database     │   │     Cache     │
       └────────────────┘   └───────┬───────┘
                                    │
                                    ▼
                              ┌──────────────┐
                              │    Celery    │
                              │ Background   │
                              │    Tasks     │
                              └──────────────┘
```

The Flask application initializes the database, JWT manager, mail service, cache, CORS, and application routes during startup.

---

## 🛠️ Tech Stack

### Frontend

| Technology | Purpose                           |
| ---------- | --------------------------------- |
| Vue 3      | Frontend framework                |
| Vite       | Development server and build tool |
| Vue Router | Client-side routing               |
| Axios      | HTTP/API communication            |
| JavaScript | Application logic                 |

The current frontend uses Vue 3, Axios, Vue Router and Vite.

### Backend

| Technology         | Purpose                      |
| ------------------ | ---------------------------- |
| Python             | Backend programming language |
| Flask              | REST API framework           |
| Flask-SQLAlchemy   | Database ORM                 |
| SQLite             | Relational database          |
| Flask-JWT-Extended | JWT authentication           |
| Flask-CORS         | Cross-origin requests        |
| Flask-Mail         | Email functionality          |
| Redis              | Caching                      |
| Celery             | Background task processing   |
| Werkzeug           | Password hashing             |

### Documentation

* OpenAPI 3
* `backend/api.yaml`

The repository includes an OpenAPI specification named **Campus Hire**, with the local API server configured at `http://localhost:5000`.

---

## 🗄️ Database Design

The application uses SQLAlchemy models for the main entities.

### Core Entities

```text
Admin
  │
  │ manages
  ▼
Company ────────────► PlacementDrive
                         │
                         │
                         ▼
                     Application
                         ▲
                         │
                         │
                      Student
```

### Main Models

#### Admin

Stores administrator credentials.

#### Student

Stores:

* Email
* Roll number
* Name
* Password
* Address
* Branch
* CGPA
* Graduation year
* Resume link
* Account status

#### Company

Stores:

* Company name
* Email
* Website
* Description
* Address
* HR name
* HR email
* HR phone number
* Approval status

#### PlacementDrive

Stores:

* Company
* Job title
* Job description
* Eligible branches
* Minimum CGPA
* Eligible graduation year
* Application deadline
* Drive status

#### Application

Connects students with placement drives and stores:

* Student
* Placement drive
* Application date
* Application status
* Remarks

Application statuses include:

```text
Applied
Shortlisted
Selected
Rejected
```

The database also enforces a unique student/drive combination so a student cannot create duplicate applications for the same placement drive.

---

## ⚡ Caching

Redis is used as the application's caching layer.

Frequently accessed endpoints use caching to reduce repeated database queries and improve response performance.

For example, dashboard and company-related endpoints use short-lived cache entries.

Default Redis configuration:

```text
Host: localhost
Port: 6379
Database: 0
```

---

## ⏱️ Background Tasks

Celery is used for asynchronous and scheduled operations.

The project includes tasks for:

* Email notifications
* Placement-drive reminders
* Monthly placement activity reports
* CSV generation
* Scheduled communication with students

For example, the daily reminder task identifies active placement drives and sends students an email containing the available drives and application deadlines.

---

## 📧 Email Notifications

The backend contains an email service used by Celery tasks for automated communication.

Examples include:

* Active placement-drive notifications
* Monthly placement reports
* Other system notifications

For production usage, email credentials should be supplied through environment variables rather than committed to the repository.

---

## 📂 Project Structure

```text
placement_portal_23f3003203/
│
├── backend/
│   │
│   ├── controllers/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── company.py
│   │   └── user.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── cache.py
│   │   ├── celery.py
│   │   ├── mail.py
│   │   ├── queries.py
│   │   ├── redis.py
│   │   └── tasks.py
│   │
│   ├── templates/
│   │
│   ├── api.yaml
│   ├── app.py
│   ├── config.py
│   └── routes.py
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── admin/
│   │   ├── company/
│   │   ├── components/
│   │   ├── user/
│   │   ├── App.vue
│   │   ├── api.js
│   │   ├── main.js
│   │   └── router.js
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── LICENSE
└── README.md
```

The repository separates the Flask backend and Vue frontend into dedicated directories, with backend controllers divided by role and frontend pages grouped into admin, company, and student areas.

---

# 🚀 Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js
* npm
* Redis
* Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/23f3003203/placement_portal_23f3003203.git

cd placement_portal_23f3003203
```

---

# 🐍 Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-mail flask-caching redis celery werkzeug
```

> If you add a `requirements.txt` file to the repository, replace the command above with `pip install -r requirements.txt`.

---

# 🔴 Start Redis

Make sure Redis is running locally:

```bash
redis-server
```

The application expects Redis on:

```text
localhost:6379
```

---

# ⚙️ Environment Configuration

Create a `.env` file for sensitive configuration.

Example:

```env
JWT_SECRET_KEY=your-secret-key

MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

REDIS_HOST=localhost
REDIS_PORT=6379
```

**Never commit real passwords, API keys, JWT secrets, SMTP credentials, or other secrets to GitHub.**

---

# ▶️ Start the Backend

From the `backend` directory:

```bash
python app.py
```

The API will be available at:

```text
http://localhost:5000
```

The application uses Flask's application factory and initializes the database and services during startup.

---

# 💻 Frontend Setup

Open a new terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend is powered by Vite.

---

## 🏭 Production Build

Create an optimized frontend build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

---

# 🔌 API Structure

The backend organizes APIs into role-based Flask blueprints:

```text
/api/auth
/api/user
/api/company
/api/admin
```

These blueprints are registered in the Flask application through `routes.py`.

### Authentication

```http
POST /api/auth/login
```

### Student APIs

```text
/api/user/*
```

Examples:

```http
GET /api/user/get-profile
PUT /api/user/update-profile
GET /api/user/get-active-drives
GET /api/user/get-drive/<id>
GET /api/user/get-active-companies
GET /api/user/apply-drive/<drive_id>
```

### Company APIs

```text
/api/company/*
```

Examples include company registration, dashboard, profile management and placement-drive creation.

### Admin APIs

```text
/api/admin/*
```

Examples:

```http
PATCH /api/admin/admin/approve-company/<id>
PATCH /api/admin/admin/reject-company/<id>
PUT /api/admin/admin/approve-drive/<id>
PUT /api/admin/admin/block-drive/<id>
```

The complete API specification is available in:

```text
backend/api.yaml
```

---

# 🔄 Placement Workflow

The typical placement workflow is:

```text
Company Registration
        │
        ▼
   Admin Review
        │
   ┌────┴────┐
   │         │
Approve    Reject
   │
   ▼
Create Placement Drive
   │
   ▼
Admin Reviews Drive
   │
   ▼
Drive Approved
   │
   ▼
Students View Drive
   │
   ▼
Eligibility Check
   │
   ▼
Student Applies
   │
   ▼
Company Reviews Applications
   │
   ├──────────────┐
   ▼              ▼
Shortlisted     Rejected
   │
   ▼
Selected
```

---

# 📊 Application Status

Applications progress through the following states:

```text
Applied
   │
   ▼
Shortlisted
   │
   ▼
Selected
```

An application can also be marked:

```text
Rejected
```

These statuses are represented directly in the database model.

---

# 🧪 Development

For API testing, the project includes an OpenAPI specification:

```text
backend/api.yaml
```

You can import this file into tools such as:

* Swagger UI
* Postman
* Insomnia

to explore and test the API endpoints.

---

# 🔒 Security Considerations

The application implements several security mechanisms:

* Password hashing using Werkzeug
* JWT authentication
* Role-based authorization
* Protected API routes
* Student/company/admin separation
* Input validation
* Database constraints

However, before production deployment, additional hardening is recommended:

* Move all secrets to environment variables
* Rotate any credentials previously committed to Git
* Disable Flask debug mode
* Restrict CORS origins
* Enable HTTPS
* Configure secure JWT cookies/tokens
* Use a production database
* Add rate limiting
* Add centralized error logging

---

# 🚀 Future Improvements

Possible improvements include:

* [ ] Add `requirements.txt`
* [ ] Add Docker/Docker Compose support
* [ ] Add automated tests
* [ ] Add CI/CD with GitHub Actions
* [ ] Add password reset functionality
* [ ] Add email verification
* [ ] Add resume file uploads
* [ ] Add advanced placement analytics
* [ ] Add notification center
* [ ] Add company search and filtering
* [ ] Add student search and filtering
* [ ] Add interview scheduling
* [ ] Add automated eligibility matching
* [ ] Add pagination to large datasets
* [ ] Add production PostgreSQL support
* [ ] Add API rate limiting
* [ ] Improve API documentation with Swagger UI

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add your feature"
```

5. Push the branch

```bash
git push origin feature/your-feature
```

6. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Afzal Jamal**

GitHub: [23f3003203](https://github.com/afzal-10-02)

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

**CampusHire — Simplifying campus placements through technology.**
