#!/bin/bash
# setup.sh – Bootstrap script for Django project

echo "🚀 Starting Django project setup..."

# Exit immediately if a command exits with a non-zero status
set -e

# -----------------------------
# 1. Create Virtual Environment
# -----------------------------
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "🔑 Activating virtual environment..."
source venv/bin/activate

# -----------------------------
# 2. Install Dependencies
# -----------------------------
echo "📥 Installing dependencies..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi
if [ -f "requirements-dev.txt" ]; then
  pip install -r requirements-dev.txt
fi

# -----------------------------
# 3. Environment Setup
# -----------------------------
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo "⚙️ Creating .env file from template..."
  cp .env.example .env
fi

# -----------------------------
# 4. Database Migrations
# -----------------------------
echo "🗄️ Applying migrations..."
python manage.py migrate

# -----------------------------
# 5. Collect Static Files
# -----------------------------
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# -----------------------------
# 6. Run Development Server
# -----------------------------
echo "✅ Setup complete! Starting development server..."
python manage.py runserver
