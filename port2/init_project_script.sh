#!/bin/bash

################################################################################
# Portfolio Web Application - Project Initialization Script
#
# This script initializes a complete Django portfolio project from scratch:
# - Creates directory structure
# - Generates all configuration files
# - Creates Django models, admin, views, URLs
# - Sets up Docker configuration
# - Creates documentation
#
# Usage: ./init-project.sh [project-name]
#
# Requirements: git, python3
################################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
PROJECT_NAME="${1:-portfolio_project}"
CURRENT_DIR=$(pwd)

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    printf "${CYAN}║${NC} %-74s ${CYAN}║${NC}\n" "$1"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}→${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

create_file() {
    local filepath="$1"
    local content="$2"
    
    # Create parent directory if needed
    mkdir -p "$(dirname "$filepath")"
    
    # Write content to file
    echo "$content" > "$filepath"
    
    print_success "Created: $filepath"
}

################################################################################
# Banner
################################################################################

clear
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ ██╗     ██╗ ██████╗ ║
║   ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║     ██║██╔═══██╗║
║   ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██║   ██║██║     ██║██║   ██║║
║   ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██║   ██║██║     ██║██║   ██║║
║   ██║     ╚██████╔╝██║  ██║   ██║   ██║     ╚██████╔╝███████╗██║╚██████╔╝║
║   ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ║
║                                                                           ║
║              Professional Portfolio Web Application Generator            ║
║                     PWA-DSD-001 v0.2 Specification                       ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF

echo ""
print_info "Project Name: ${MAGENTA}$PROJECT_NAME${NC}"
print_info "Location: ${MAGENTA}$CURRENT_DIR/$PROJECT_NAME${NC}"
echo ""

sleep 2

################################################################################
# Step 1: Create Directory Structure
################################################################################

print_header "Step 1: Creating Directory Structure"

DIRECTORIES=(
    "$PROJECT_NAME"
    "$PROJECT_NAME/apps"
    "$PROJECT_NAME/apps/core"
    "$PROJECT_NAME/apps/core/management"
    "$PROJECT_NAME/apps/core/management/commands"
    "$PROJECT_NAME/apps/core/migrations"
    "$PROJECT_NAME/apps/core/templatetags"
    "$PROJECT_NAME/config"
    "$PROJECT_NAME/static"
    "$PROJECT_NAME/static/css"
    "$PROJECT_NAME/static/js"
    "$PROJECT_NAME/static/images"
    "$PROJECT_NAME/static/fonts"
    "$PROJECT_NAME/templates"
    "$PROJECT_NAME/templates/base"
    "$PROJECT_NAME/templates/components"
    "$PROJECT_NAME/templates/pages"
    "$PROJECT_NAME/templates/errors"
    "$PROJECT_NAME/media"
    "$PROJECT_NAME/media/profile"
    "$PROJECT_NAME/media/projects"
    "$PROJECT_NAME/media/blog"
    "$PROJECT_NAME/media/certifications"
    "$PROJECT_NAME/data"
    "$PROJECT_NAME/data/fixtures"
    "$PROJECT_NAME/docker"
    "$PROJECT_NAME/docs"
    "$PROJECT_NAME/logs"
    "$PROJECT_NAME/tests"
    "$PROJECT_NAME/.github"
    "$PROJECT_NAME/.github/workflows"
)

for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "$dir"
done

print_success "Created ${#DIRECTORIES[@]} directories"

# Create __init__.py files for Python packages
touch "$PROJECT_NAME/apps/__init__.py"
touch "$PROJECT_NAME/apps/core/__init__.py"
touch "$PROJECT_NAME/apps/core/migrations/__init__.py"
touch "$PROJECT_NAME/apps/core/management/__init__.py"
touch "$PROJECT_NAME/apps/core/management/commands/__init__.py"
touch "$PROJECT_NAME/apps/core/templatetags/__init__.py"

print_success "Created Python package markers"

################################################################################
# Step 2: Generate Configuration Files
################################################################################

print_header "Step 2: Generating Configuration Files"

# requirements.txt
cat > "$PROJECT_NAME/requirements.txt" << 'EOF'
# Core Django
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
Pillow==10.2.0

# Production
gunicorn==21.2.0

# Development
django-debug-toolbar==4.3.0
django-extensions==3.2.3

# Testing
pytest==8.0.2
pytest-django==4.8.0
pytest-cov==4.1.0

# Code Quality
black==24.2.0
flake8==7.0.0
isort==5.13.2
EOF

print_success "Created: requirements.txt"

# .env.example
cat > "$PROJECT_NAME/.env.example" << 'EOF'
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3
# DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Security (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Cloud Storage (Optional)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1

# Analytics
ENABLE_ANALYTICS=False
GOOGLE_ANALYTICS_ID=
EOF

print_success "Created: .env.example"

# .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/
.eggs/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static_collected

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Docker
docker-compose.override.yml

# Logs
logs/*.log
EOF

print_success "Created: .gitignore"

# Dockerfile
cat > "$PROJECT_NAME/docker/Dockerfile" << 'EOF'
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
EOF

print_success "Created: docker/Dockerfile"

# docker-compose.yml
cat > "$PROJECT_NAME/docker-compose.yml" << 'EOF'
version: '3.8'

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
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
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
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:
EOF

print_success "Created: docker-compose.yml"

# nginx.conf
cat > "$PROJECT_NAME/docker/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;
        client_max_body_size 5M;

        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }
    }
}
EOF

print_success "Created: docker/nginx.conf"

# pytest.ini
cat > "$PROJECT_NAME/pytest.ini" << 'EOF'
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = --cov=apps --cov-report=html --cov-report=term-missing
testpaths = tests apps
EOF

print_success "Created: pytest.ini"

# .flake8
cat > "$PROJECT_NAME/.flake8" << 'EOF'
[flake8]
max-line-length = 88
exclude = 
    .git,
    __pycache__,
    venv,
    env,
    migrations,
    settings.py
ignore = E203, E266, W503
EOF

print_success "Created: .flake8"

# pyproject.toml (black and isort config)
cat > "$PROJECT_NAME/pyproject.toml" << 'EOF'
[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?
extend-exclude = '''
/(
  | migrations
  | venv
  | env
)/
'''

[tool.isort]
profile = "black"
line_length = 88
skip_gitignore = true
known_django = "django"
sections = ["FUTURE", "STDLIB", "DJANGO", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
EOF

print_success "Created: pyproject.toml"

# Makefile
cat > "$PROJECT_NAME/Makefile" << 'EOF'
.PHONY: help install migrate run test clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make migrate       - Run database migrations"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean Python cache files"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

format:
	black .
	isort .

lint:
	flake8 .
	black --check .
	isort --check .
EOF

print_success "Created: Makefile"

################################################################################
# Step 3: Generate README and Documentation
################################################################################

print_header "Step 3: Generating Documentation"

# README.md
cat > "$PROJECT_NAME/README.md" << 'EOF'
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

Your Name - [@yourhandle](https://github.com/yourhandle)
EOF

print_success "Created: README.md"

# LICENSE
cat > "$PROJECT_NAME/LICENSE" << 'EOF'
MIT License

Copyright (c) 2024 Portfolio Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

print_success "Created: LICENSE"

# CHANGELOG.md
cat > "$PROJECT_NAME/CHANGELOG.md" << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial project setup
- Django models for Portfolio, Skills, Projects, Experience
- SFIA skills framework implementation (L1-L7)
- STAR method for experience and projects
- Django admin customization
- Docker configuration
- REST API endpoints

### Changed
- N/A

### Fixed
- N/A

## [0.1.0] - 2024-01-01

### Added
- Project initialization
EOF

print_success "Created: CHANGELOG.md"

################################################################################
# Step 4: Generate GitHub Actions CI/CD
################################################################################

print_header "Step 4: Setting Up CI/CD"

cat > "$PROJECT_NAME/.github/workflows/ci.yml" << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run linting
      run: |
        flake8 .
        black --check .
        isort --check .
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        SECRET_KEY: test-secret-key
        DEBUG: False
      run: |
        pytest --cov=apps --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -f docker/Dockerfile -t portfolio:latest .
    
    - name: Test Docker image
      run: docker run --rm portfolio:latest python manage.py check
EOF

print_success "Created: .github/workflows/ci.yml"

################################################################################
# Step 5: Copy Django Files from Previous Artifacts
################################################################################

print_header "Step 5: Creating Django Application Files"

print_info "Generating placeholder files..."
print_info "Note: Copy the full model/admin/settings code from the artifacts provided earlier"

# Create placeholder files
touch "$PROJECT_NAME/apps/core/models.py"
touch "$PROJECT_NAME/apps/core/admin.py"
touch "$PROJECT_NAME/apps/core/views.py"
touch "$PROJECT_NAME/apps/core/urls.py"
touch "$PROJECT_NAME/apps/core/serializers.py"
touch "$PROJECT_NAME/apps/core/context_processors.py"
touch "$PROJECT_NAME/apps/core/sitemaps.py"

cat > "$PROJECT_NAME/apps/core/models.py" << 'EOF'
# apps/core/models.py
# TODO: Copy complete models.py content from artifacts
# Includes: Profile, SkillArea, Skill, Education, Experience, Project, etc.

from django.db import models

# Placeholder - Replace with full content
EOF

cat > "$PROJECT_NAME/apps/core/admin.py" << 'EOF'
# apps/core/admin.py
# TODO: Copy complete admin.py content from artifacts

from django.contrib import admin

# Placeholder - Replace with full content
EOF

print_success "Created Django app files (placeholders)"
print_warning "Remember to copy full content from provided artifacts!"

################################################################################
# Step 6: Create Manage.py and WSGI
################################################################################

print_header "Step 6: Creating Django Entry Points"

cat > "$PROJECT_NAME/manage.py" << 'EOF'
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
EOF

chmod +x "$PROJECT_NAME/manage.py"
print_success "Created: manage.py"

cat > "$PROJECT_NAME/config/__init__.py" << 'EOF'
# Django project initialization
EOF

cat > "$PROJECT_NAME/config/wsgi.py" << 'EOF'
"""
WSGI config for portfolio project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
EOF

print_success "Created: config/wsgi.py"

cat > "$PROJECT_NAME/config/asgi.py" << 'EOF'
"""
ASGI config for portfolio project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_asgi_application()
EOF

print_success "Created: config/asgi.py"

################################################################################
# Step 7: Create Management Commands
################################################################################

print_header "Step 7: Creating Management Commands"

cat > "$PROJECT_NAME/apps/core/management/commands/export_json.py" << 'EOF'
# Management command to export data to JSON
# TODO: Copy full export_json.py content from artifacts

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export portfolio data to JSON files'
    
    def handle(self, *args, **options):
        self.stdout.write('Exporting data...')
        # TODO: Implement export logic
EOF

print_success "Created: management commands"

################################################################################
# Completion
################################################################################

print_header "🎉 Project Initialization Complete!"

echo ""
print_success "Project structure created successfully!"
echo ""

print_info "Project Details:"
echo "  ${CYAN}Name:${NC} $PROJECT_NAME"
echo "  ${CYAN}Location:${NC} $CURRENT_DIR/$PROJECT_NAME"
echo "  ${CYAN}Files Created:${NC} $(find "$PROJECT_NAME" -type f | wc -l)"
echo ""

print_info "Next Steps:"
echo ""
echo "  ${GREEN}1.${NC} Navigate to project:"
echo "     ${CYAN}cd $PROJECT_NAME${NC}"
echo ""
echo "  ${GREEN}2.${NC} Copy Django code from artifacts:"
echo "     ${CYAN}# Copy models.py, admin.py, settings.py, etc.${NC}"
echo ""
echo "  ${GREEN}3.${NC} Run development setup:"
echo "     ${CYAN}chmod +x dev-setup.sh${NC}"
echo "     ${CYAN}./dev-setup.sh${NC}"
echo ""
echo "  ${GREEN}4.${NC} Start development server:"
echo "     ${CYAN}source venv/bin/activate${NC}"
echo "     ${CYAN}python manage.py runserver${NC}"
echo ""

print_info "Important Files to Update:"
echo ""
echo "  ${YELLOW}→${NC} apps/core/models.py     ${CYAN}(Copy from artifact: django_models)${NC}"
echo "  ${YELLOW}→${NC} apps/core/admin.py      ${CYAN}(Copy from artifact: django_admin)${NC}"
echo "  ${YELLOW}→${NC} config/settings.py      ${CYAN}(Copy from artifact: django_settings)${NC}"
echo "  ${YELLOW}→${NC} apps/core/urls.py       ${CYAN}(Copy from artifact: django_urls_context)${NC}"
echo "  ${YELLOW}→${NC} .env                    ${CYAN}(Copy from .env.example and update)${NC}"
echo ""

print_warning "Don't forget to:"
echo "  - Initialize Git repository: ${CYAN}git init${NC}"
echo "  - Create initial commit: ${CYAN}git add . && git commit -m 'Initial commit'${NC}"
echo "  - Set up remote: ${CYAN}git remote add origin <url>${NC}"
echo ""

print_success "Happy coding! 🚀"
echo ""