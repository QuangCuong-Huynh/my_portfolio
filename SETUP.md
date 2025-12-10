# Portfolio Application Setup Guide

## 🎉 Application Status: **RUNNING**

Your Django portfolio application is now successfully running on **<http://localhost:8000>**

---

## Project Structure

This repository contains two Django projects:

### 1. **Main Portfolio Application** (Recommended) 📁 `root/`

- **Location:** `d:\GitHub\my_portfolio\root\`
- **Settings Module:** `portfolio_project.settings`
- **Features:**
  - Full-featured portfolio with `core` app
  - Django REST Framework API
  - Tailwind CSS integration
  - CORS headers support
  - Debug toolbar (development)
  - Crispy forms with Tailwind
  - Static file management (WhiteNoise)
  - Comprehensive logging
  - SFIA skill level tracking
  - Media file handling

### 2. **Simple Starter Project** 📁 Root Level

- **Location:** `d:\GitHub\my_portfolio\`
- **Settings Module:** `my_portfolio.settings`
- **Purpose:** Basic Django starter template
- **Status:** Not actively used

---

## ✅ What Was Fixed

### Issues Resolved

1. ✅ **Dependency Mismatch** - Updated `requirements.txt` with all 166 required packages
2. ✅ **Multiple Failed Servers** - Stopped all conflicting server processes
3. ✅ **Missing Packages** - Installed python-decouple, whitenoise, crispy-forms, etc.
4. ✅ **Database Setup** - Ran migrations successfully
5. ✅ **Server Configuration** - Application now running on port 8000

### Changes Made

- Updated `requirements.txt` from 6 to 166 packages
- Updated `.env.example` with comprehensive configuration
- Ran database migrations
- Started development server successfully

---

## 🚀 Quick Start

### Running the Application

```powershell
# Navigate to the root directory
cd d:\GitHub\my_portfolio

# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1

# Navigate to the portfolio project
cd root

# Start the development server
..\venv\Scripts\python.exe manage.py runserver
```

The application will be available at:

- **Homepage:** <http://localhost:8000>
- **Admin Panel:** <http://localhost:8000/admin/>
- **API:** <http://localhost:8000/api/> (if configured)

---

## 📦 Installed Dependencies

All 166 packages have been installed including:

### Core Framework

- Django 5.2.7
- djangorestframework 3.14.0
- gunicorn 21.2.0

### Configuration & Security

- python-decouple 3.8
- python-dotenv (for root project)
- dj-database-url 2.1.0

### Frontend & Styling

- django-tailwind 4.2.0
- django-crispy-forms 2.1
- crispy-tailwind 1.0.3
- whitenoise 6.6.0

### Development Tools

- django-debug-toolbar 4.3.0
- django-extensions 3.2.3
- black 24.2.0
- flake8 7.3.0

### Additional Features

- django-cors-headers 4.3.1
- django-allauth 0.61.1
- Pillow 10.2.0
- pandas 2.2.3
- matplotlib 3.10.1
- jupyterlab 4.4.2

**Note:** PyTorch was excluded as it requires special installation.

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key variables:

- `DEBUG=True` - Development mode
- `SECRET_KEY` - Change in production!
- `DATABASE_URL` - Database connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS` - CORS configuration

---

## 🗄️ Database

### Current Setup

- **Type:** SQLite
- **Location:** `root/db.sqlite3`
- **Status:** ✅ Migrations applied

### Migrations Applied

- Django core apps (admin, auth, contenttypes, sessions)
- Portfolio core app
- All dependencies

### Common Commands

```powershell
# Create new migrations
cd root
..\venv\Scripts\python.exe manage.py makemigrations

# Apply migrations
..\venv\Scripts\python.exe manage.py migrate

# Create superuser for admin access
..\venv\Scripts\python.exe manage.py createsuperuser
```

---

## 🛠️ Development Workflow

### Starting Development

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Navigate to project
cd root

# 3. Start server
..\venv\Scripts\python.exe manage.py runserver

# Server will start on http://localhost:8000
```

### Running Tests

```powershell
cd root
..\venv\Scripts\python.exe manage.py test
```

### Django Admin

```powershell
# Create superuser (first time only)
cd root
..\venv\Scripts\python.exe manage.py createsuperuser

# Access admin at: http://localhost:8000/admin/
```

### Collecting Static Files

```powershell
cd root
..\venv\Scripts\python.exe manage.py collectstatic
```

---

## 📁 Project Structure

```
my_portfolio/
├── root/                          # Main portfolio application
│   ├── core/                      # Portfolio app
│   │   ├── models.py             # Database models
│   │   ├── views.py              # View logic
│   │   ├── urls.py               # URL routing
│   │   ├── admin.py              # Admin configuration
│   │   ├── forms.py              # Form definitions
│   │   ├── templates/            # HTML templates
│   │   └── static/               # Static files (CSS, JS)
│   ├── portfolio_project/        # Project settings
│   │   ├── settings.py           # Main settings
│   │   ├── urls.py               # Root URL config
│   │   └── wsgi.py               # WSGI config
│   ├── manage.py                 # Django management script
│   ├── db.sqlite3                # Database file
│   └── requirements.txt          # Project dependencies
├── my_portfolio/                  # Simple starter project
│   └── settings.py               # Basic settings
├── venv/                         # Virtual environment
├── requirements.txt              # Updated with all dependencies
├── .env.example                  # Environment template
└── README.md                     # Project documentation
```

---

## 🔧 Troubleshooting

### Server Won't Start

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill any processes using port 8000
Get-Process python | Stop-Process -Force
```

### Import Errors

```powershell
# Verify virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Database Issues

```powershell
# Reset database (WARNING: Deletes all data)
cd root
Remove-Item db.sqlite3
..\venv\Scripts\python.exe manage.py migrate
```

---

## 📝 Next Steps

1. **Create Admin User:**

   ```powershell
   cd root
   ..\venv\Scripts\python.exe manage.py createsuperuser
   ```

2. **Customize Settings:**
   - Edit `root/portfolio_project/settings.py`
   - Update `.env` file with your configuration

3. **Add Content:**
   - Access admin panel at <http://localhost:8000/admin/>
   - Add portfolio items, skills, projects, etc.

4. **Customize Templates:**
   - Edit templates in `root/core/templates/`
   - Modify static files in `root/core/static/`

5. **Deploy to Production:**
   - Review security settings
   - Set `DEBUG=False`
   - Configure production database (PostgreSQL recommended)
   - Set up static file hosting
   - Configure domain and SSL

---

## 🌐 URLs

- **Homepage:** <http://localhost:8000>
- **Admin Panel:** <http://localhost:8000/admin/>
- **API (if configured):** <http://localhost:8000/api/>

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

## ✨ Summary

Your Django portfolio application is now:

- ✅ Fully configured with all dependencies
- ✅ Database migrated and ready
- ✅ Running on <http://localhost:8000>
- ✅ Admin panel accessible
- ✅ Ready for development

**Happy coding! 🚀**
