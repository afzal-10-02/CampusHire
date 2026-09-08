# 🚀 How to Run the Application

Follow the steps below to run **CampusHire** locally.

## 📋 Prerequisites

Make sure the following are installed on your system:

* **Python 3.10+**
* **Node.js 18+**
* **npm**
* **Redis**
* **Git**

---

## 1. Clone the Repository

```bash
git clone https://github.com/23f3003203/placement_portal_23f3003203.git

cd placement_portal_23f3003203
```

---

# 🐍 2. Setup the Backend

Open a terminal and navigate to the backend:

```bash
cd backend
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Install Dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-mail flask-caching redis celery werkzeug python-dotenv
```

---

# ⚙️ 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

MAIL_USERNAME=your-email
MAIL_PASSWORD=your-email-password

REDIS_HOST=localhost
REDIS_PORT=6379
```

> ⚠️ **Do not commit `.env` to GitHub.** Add it to `.gitignore`.

---

# 🔴 4. Start Redis

CampusHire uses Redis for caching and Celery background tasks.

Make sure Redis is running on:

```text
localhost:6379
```

Start Redis:

```bash
redis-server
```

If you are using Windows and Redis is installed as a service, make sure the Redis service is running before starting the application.

---

# ▶️ 5. Start the Backend

Open a terminal in the `backend` directory:

```bash
python app.py
```

The Flask backend should start on:

```text
http://localhost:5000
```

You can test the backend by opening:

```text
http://localhost:5000
```

---

# ⏱️ 6. Start Celery

Celery is used for background tasks such as email notifications and scheduled jobs.

Keep Redis running and open **another terminal**.

Navigate to the backend:

```bash
cd backend
```

Activate the virtual environment again if necessary:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

Start the Celery worker:

```bash
celery -A services.celery.celery worker --loglevel=info
```

Keep this terminal running.

> If the Celery object is exposed under a different module/object name in your local version, use the corresponding `-A module.object` path.

---

# 💻 7. Setup the Frontend

Open another terminal.

From the project root:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Vite will display the local frontend URL in the terminal, normally:

```text
http://localhost:5173
```

---

# 🖥️ 8. Run the Complete Application

You should now have the following services running:

### Terminal 1 — Redis

```bash
redis-server
```

### Terminal 2 — Flask Backend

```bash
cd backend
venv\Scripts\activate
python app.py
```

### Terminal 3 — Celery Worker

```bash
cd backend
venv\Scripts\activate
celery -A services.celery.celery worker --loglevel=info
```

### Terminal 4 — Vue Frontend

```bash
cd frontend
npm run dev
```

---

## 🌐 Application URLs

| Service     | URL                     |
| ----------- | ----------------------- |
| Frontend    | `http://localhost:5173` |
| Backend API | `http://localhost:5000` |
| Redis       | `localhost:6379`        |

Open the frontend in your browser:

```text
http://localhost:5173
```

---

# 🗂️ Project Structure

```text
placement_portal_23f3003203/
│
├── backend/
│   ├── controllers/
│   ├── database/
│   ├── services/
│   ├── templates/
│   ├── app.py
│   ├── config.py
│   └── routes.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── LICENSE
└── README.md
```

---

# 🛑 Stopping the Application

To stop each service, press:

```text
Ctrl + C
```

Stop:

1. Vite frontend
2. Celery worker
3. Flask backend
4. Redis

---

# 🐛 Troubleshooting

### Redis connection error

If you see an error similar to:

```text
Connection refused
```

make sure Redis is running:

```bash
redis-server
```

---

### Python module not found

Make sure the virtual environment is activated:

```bash
venv\Scripts\activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

### Frontend dependencies error

Delete `node_modules` and reinstall:

```bash
rm -rf node_modules
npm install
```

On Windows PowerShell:

```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

---

### Port already in use

If port `5000` or `5173` is already being used, stop the process using that port or configure the application to use another port.

---

## ✅ Quick Start

Once everything is configured, the usual development workflow is:

```bash
# Terminal 1
redis-server
```

```bash
# Terminal 2
cd backend
venv\Scripts\activate
python app.py
```

```bash
# Terminal 3
cd backend
venv\Scripts\activate
celery -A services.celery.celery worker --loglevel=info
```

```bash
# Terminal 4
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

🎉 **CampusHire is now running locally.**
