#!/usr/bin/env python3
"""
Portfolio Web Application - Project Setup Script
Creates complete Django project structure following PWA-DSD-001 v0.2 specification
"""

import os
import subprocess
import sys

def create_directory_structure():
    """Create the complete project directory structure"""
    directories = [
        'portfolio_project',
        'portfolio_project/apps',
        'portfolio_project/apps/core',
        'portfolio_project/apps/resume',
        'portfolio_project/apps/blog',
        'portfolio_project/apps/projects',
        'portfolio_project/apps/certifications',
        'portfolio_project/static',
        'portfolio_project/static/css',
        'portfolio_project/static/js',
        'portfolio_project/static/images',
        'portfolio_project/templates',
        'portfolio_project/templates/base',
        'portfolio_project/templates/components',
        'portfolio_project/templates/pages',
        'portfolio_project/media',
        'portfolio_project/data',
        'portfolio_project/config',
        'docker',
        'docs',
        'tests',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")

def create_requirements_txt():
    """Create requirements.txt with all dependencies"""
    requirements = """# Core Django
Django==5.0.3
python-decouple==3.8
whitenoise==6.6.0

# Database
psycopg2-binary==2.9.9
dj-database-url==2.1.0

# REST Framework (optional for API)
djangorestframework==3.14.0
django-cors-headers==4.3.1

# Content & Forms
django-markdown-deux==1.0.5
django-crispy-forms==2.1
crispy-tailwind==1.0.3

# Storage & Media
Pillow==10.2.0

# Security & Authentication
django-allauth==0.61.1

# Development
django-debug-toolbar==4.3.0
django-extensions==3.2.3

# Production
gunicorn==21.2.0
django-storages==1.14.2

# Testing
pytest==8.0.2
pytest-django==4.8.0
pytest-cov==4.1.0
factory-boy==3.3.0

# Code Quality
black==24.2.0
flake8==7.0.0
isort==5.13.2
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✓ Created: requirements.txt")

def create_env_example():
    """Create .env.example file"""
    env_content = """# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Optional: SQLite for development
# DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (for contact form)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# Static Files
STATIC_ROOT=staticfiles/
MEDIA_ROOT=media/

# Security (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Cloud Storage (Optional - Azure/AWS S3)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    print("✓ Created: .env.example")

def create_dockerfile():
    """Create Dockerfile for containerization"""
    dockerfile_content = """FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=portfolio_project.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    gcc \\
    python3-dev \\
    musl-dev \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "portfolio_project.wsgi:application"]
"""
    
    with open('docker/Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    print("✓ Created: docker/Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml"""
    compose_content = """version: '3.8'

services:
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: portfolio_db
      POSTGRES_USER: portfolio_user
      POSTGRES_PASSWORD: portfolio_pass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portfolio_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: docker/Dockerfile
    command: gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)
    print("✓ Created: docker-compose.yml")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Docker
docker-compose.override.yml
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created: .gitignore")

def create_readme():
    """Create comprehensive README.md"""
    readme_content = """# Portfolio Web Application

Professional portfolio platform built with Django and Tailwind CSS following enterprise-grade design specifications (PWA-DSD-001 v0.2).

## Features

- 📝 **Resume/CV Module** - SFIA-based skills framework (L1-L7)
- 📰 **Blog System** - Markdown support with categories and tags
- 💼 **Project Showcase** - STAR method for presentation
- 🏆 **Certifications & Awards** - Evidence-based verification
- 📱 **Responsive Design** - Mobile-first with Tailwind CSS
- 🔒 **Security** - CSRF/XSS protection, HTTPS enforcement
- 🐳 **Dockerized** - Ready for cloud deployment

## Tech Stack

- **Backend**: Django 5.0 (Python 3.12)
- **Frontend**: Tailwind CSS 3.x
- **Database**: PostgreSQL 16
- **Deployment**: Docker + Gunicorn + Nginx
- **Cloud**: Azure/AWS/Railway compatible

## Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd portfolio_project
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_data  # Optional: load sample data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

### 5. Docker Deployment

```bash
docker-compose up -d --build
```

## Project Structure

```
portfolio_project/
├── apps/
│   ├── core/           # Base models, utilities
│   ├── resume/         # Profile, Skills, Experience
│   ├── blog/           # Blog posts, categories
│   ├── projects/       # Project showcase
│   └── certifications/ # Certs & awards
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── data/               # JSON data files
├── config/             # Settings, URLs
├── docker/             # Docker configs
└── tests/              # Test suite
```

## Key Components

### Skills Framework (SFIA)

Skills are structured using SFIA levels:
- **L1**: Entry - Follow
- **L2**: Foundation - Assist
- **L3**: Practitioner - Apply
- **L4**: Senior - Enable
- **L5**: Lead - Ensure/Advise
- **L6**: Principal - Initiate/Influence
- **L7**: Expert - Set Strategy

### STAR Method

Experience and Projects use STAR structure:
- **S**ituation: Context and challenge
- **T**ask: Responsibilities and objectives
- **A**ction: Steps taken and methods used
- **R**esult: Measurable outcomes and impact

## Development

### Running Tests

```bash
pytest
pytest --cov=apps --cov-report=html
```

### Code Quality

```bash
black .
isort .
flake8
```

### Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Enable SSL (`SECURE_SSL_REDIRECT=True`)
- [ ] Configure cloud storage (S3/Azure Blob)
- [ ] Setup backup strategy
- [ ] Configure monitoring (Sentry)
- [ ] Setup CDN for static files
- [ ] Enable database backups
- [ ] Configure email backend

### Cloud Platforms

#### Azure App Service
```bash
az webapp up --runtime PYTHON:3.12 --sku B1
```

#### AWS Elastic Beanstalk
```bash
eb init -p python-3.12 portfolio
eb create portfolio-env
```

#### Railway
```bash
railway init
railway up
```

## API Documentation

REST API available at `/api/v1/` (optional)

- `/api/v1/skills/` - Skills list
- `/api/v1/projects/` - Projects
- `/api/v1/blog/` - Blog posts
- `/api/v1/certifications/` - Certifications

## Security

- CSRF tokens on all forms
- XSS protection via Django templates
- SQL injection prevention (ORM)
- HTTPS enforcement in production
- Secure password hashing (PBKDF2)
- Rate limiting on contact forms

## Performance

- Static file caching with WhiteNoise
- Database query optimization
- Redis caching (optional)
- CDN integration
- Image optimization
- Lazy loading

## License

MIT License - See LICENSE file

## Support

For issues and questions: [GitHub Issues](https://github.com/yourusername/portfolio/issues)

## Author

**Quang Cuong Huynh**
- GitHub: [@yourhandle]
- LinkedIn: [profile]
- Email: your.email@example.com
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✓ Created: README.md")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Portfolio Web Application - Project Setup")
    print("=" * 60)
    print()
    
    try:
        create_directory_structure()
        print()
        create_requirements_txt()
        create_env_example()
        create_dockerfile()
        create_docker_compose()
        create_gitignore()
        create_readme()
        
        print()
        print("=" * 60)
        print("✓ Project structure created successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. cd portfolio_project")
        print("2. python -m venv venv")
        print("3. source venv/bin/activate  # Windows: venv\\Scripts\\activate")
        print("4. pip install -r requirements.txt")
        print("5. django-admin startproject config .")
        print("6. python manage.py startapp core apps/core")
        print("7. Configure settings.py with database and apps")
        print()
        print("For Docker deployment:")
        print("docker-compose up -d --build")
        print()
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
