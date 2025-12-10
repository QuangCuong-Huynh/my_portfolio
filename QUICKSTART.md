# Quick Start Guide

## 🚀 Start the Application

```powershell
# Navigate to project root
cd d:\GitHub\my_portfolio

# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1

# Navigate to portfolio project
cd root

# Start development server
..\venv\Scripts\python.exe manage.py runserver
```

**Server will be available at:** <http://localhost:8000>

---

## 🛑 Stop the Application

Press `Ctrl + C` in the terminal running the server

Or force stop all Python processes:

```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## 🔍 Check Server Status

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# List running Python processes
Get-Process python -ErrorAction SilentlyContinue
```

---

## 📝 Common Commands

### Create Admin User

```powershell
cd root
..\venv\Scripts\python.exe manage.py createsuperuser
```

### Run Migrations

```powershell
cd root
..\venv\Scripts\python.exe manage.py migrate
```

### Collect Static Files

```powershell
cd root
..\venv\Scripts\python.exe manage.py collectstatic
```

### Run Tests

```powershell
cd root
..\venv\Scripts\python.exe manage.py test
```

### Django Shell

```powershell
cd root
..\venv\Scripts\python.exe manage.py shell
```

---

## 📚 Documentation

- Full setup guide: [SETUP.md](./SETUP.md)
- Implementation details: See artifacts in `.gemini/antigravity/brain/`

---

## ✅ Application Status

- **Dependencies:** 166 packages installed
- **Database:** SQLite (migrated)
- **Configuration:** `.env.example` (copy to `.env` for custom config)
- **Project:** `root/portfolio_project`
