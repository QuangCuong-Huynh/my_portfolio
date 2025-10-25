# 🌐 My Portfolio

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
# Portfolio Web Application

Professional portfolio platform built with Django and Tailwind CSS following enterprise-grade design specifications (PWA-DSD-001 v0.2).

## 🎯 Features

- 📝 **Resume/CV Module** - SFIA-based skills framework (L1-L7)
- 📰 **Blog System** - Markdown support with categories and tags
- 💼 **Project Showcase** - STAR method for presentation
- 🏆 **Certifications & Awards** - Evidence-based verification
- 📱 **Responsive Design** - Mobile-first with Tailwind CSS
- 🔒 **Security** - CSRF/XSS protection, HTTPS enforcement
- 🐳 **Dockerized** - Ready for cloud deployment

## 🚀 Quick Start

### Development Setup

```bash
# Run development setup
./dev-setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://localhost:8000

### Docker Setup

```bash
docker-compose up -d --build
```

## 📚 Documentation

- [Installation Guide](docs/INSTALL.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Documentation](docs/API.md)

## 🛠️ Tech Stack

- **Backend**: Django 5.0 (Python 3.12)
- **Frontend**: Tailwind CSS 3.x
- **Database**: PostgreSQL 16
- **Deployment**: Docker + Gunicorn + Nginx

## 📝 License

MIT License - See LICENSE file

## 👤 Author

Your Name - [@QuangCuong-Huynh](https://github.com/QuangCuong-Huynh)