# Portfolio Web Application - Implementation Guide

## 📋 Overview

This guide provides step-by-step instructions to implement your Portfolio Web Application following the PWA-DSD-001 v0.2 specification with SFIA skills framework and STAR method presentation.

---

## 🎯 What's Been Created

### 1. **Project Structure Setup Script** (`portfolio_setup.py`)
- Creates complete directory structure
- Generates all configuration files
- Sets up Docker and deployment configs

### 2. **Django Models** (Complete Data Layer)
- ✅ Profile model with social links
- ✅ SFIA-based Skills (L1-L7) with evidence linking
- ✅ Experience with STAR method
- ✅ Projects with STAR method
- ✅ Certifications & Awards
- ✅ Blog with Series/Categories/Tags
- ✅ Contact messages
- ✅ Site settings (singleton)

### 3. **Django Admin** (Content Management)
- ✅ Fully customized admin interface
- ✅ Color-coded SFIA badges
- ✅ STAR method fieldsets
- ✅ Evidence tracking
- ✅ Bulk actions for publishing/archiving
- ✅ Image previews and thumbnails

### 4. **Settings & Configuration**
- ✅ Production-ready Django settings
- ✅ Security configurations (HTTPS, CSRF, XSS)
- ✅ Database configuration (PostgreSQL support)
- ✅ Email settings
- ✅ Cloud storage support (AWS S3)
- ✅ Caching (Redis/Local)
- ✅ Logging configuration

### 5. **URL Routing & Sitemaps**
- ✅ Complete URL structure
- ✅ SEO-friendly sitemaps
- ✅ API endpoints for JSON data
- ✅ Custom error handlers

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Run the Setup Script

```bash
# Create project directory
mkdir portfolio-app && cd portfolio-app

# Run the setup script
python portfolio_setup.py

# Navigate to project
cd portfolio_project /apps
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Django Project

```bash
# Create Django project (if not exists)
django-admin startproject config .

# Create core app
python manage.py startapp core apps/core
```

### Step 5: Configure Settings

1. Copy the models into `apps/core/models.py`
2. Copy the admin config into `apps/core/admin.py`
3. Replace `config/settings.py` with the provided settings
4. Copy URL configurations
5. Create `.env` from `.env.example`

```bash
cp .env.example .env
nano .env  # Edit with your settings
```

### Step 6: Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 7: Load Initial Data (Optional)

```bash
# Create sample data fixture
python manage.py dumpdata --indent 2 > initial_data.json

# Or manually create via admin panel
python manage.py runserver
```

Visit: http://localhost:8000/admin

---

## 📦 What You Still Need to Create

### 1. **Views (apps/core/views.py)**

Create Django class-based views for:
- `HomeView` - Landing page
- `AboutView` - About/Resume page
- `SkillsListView` - Skills grid with filters
- `ProjectsListView` - Projects showcase
- `ExperienceListView` - Work experience
- `BlogListView` - Blog posts
- `CertificationsListView` - Certs display
- `ContactView` - Contact form
- `DemoView` - SPA demo page

### 2. **Serializers (apps/core/serializers.py)**

For REST API (optional):
```python
from rest_framework import serializers
from .models import Skill, Project, Experience

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
```

### 3. **API Views (apps/core/api_views.py)**

```python
from rest_framework import viewsets
from .models import Skill, Project
from .serializers import SkillSerializer, ProjectSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
```

### 4. **Templates**

Create HTML templates using Tailwind CSS:

```
templates/
├── base/
│   ├── base.html          # Base template
│   ├── header.html        # Navigation
│   └── footer.html        # Footer
├── pages/
│   ├── home.html          # Landing page
│   ├── about.html         # About/Resume
│   ├── skills.html        # Skills grid
│   ├── projects.html      # Projects list
│   ├── project_detail.html
│   ├── experience.html
│   ├── blog.html
│   ├── blog_post.html
│   ├── certifications.html
│   ├── contact.html
│   └── demo.html          # SPA demo
└── components/
    ├── skill_card.html
    ├── project_card.html
    ├── experience_card.html
    └── cert_card.html
```

### 5. **Static Files**

Setup Tailwind CSS:

```bash
# Install Tailwind via CDN (quick) or npm (production)

# Create tailwind.config.js
npx tailwindcss init
npm tailwindcss init

# Create input.css
mkdir -p static/css
echo '@tailwind base;' > static/css/input.css
echo '@tailwind components;' >> static/css/input.css
echo '@tailwind utilities;' >> static/css/input.css

# Build CSS
npx tailwindcss -i static/css/input.css -o static/css/output.css --watch
```

### 6. **Forms (apps/core/forms.py)**

```python
from django import forms
from crispy_forms.helper import FormHelper
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'space-y-4'
```

---

## 🎨 Frontend Integration

### Using the Existing Demo HTML

You already have a complete HTML demo (`Fixed Portfolio Demo - SFIA Skills Framework.html`). You can:

1. **Option A: Convert to Django Templates**
   - Extract sections into Django template includes
   - Replace hardcoded JSON with template variables
   - Use Django template tags for loops/conditionals

2. **Option B: Keep as Static Demo**
   - Serve the HTML file as a `/demo` route
   - Use it as a reference for styling
   - Build Django templates separately

### Sample Template Conversion

**Base Template (base.html)**:
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site_settings.site_title }}{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {% block extra_css %}{% endblock %}
</head>
<body class="bg-gray-50 dark:bg-gray-900">
    {% include 'base/header.html' %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    {% include 'base/footer.html' %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Skills Page (skills.html)**:
```django
{% extends 'base/base.html' %}
{% load humanize %}

{% block content %}
<section class="py-20 bg-white dark:bg-gray-900">
    <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-4xl font-bold mb-16">Professional Skills</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for skill in skills %}
            <div class="skill-card bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <h3 class="text-lg font-semibold mb-2">{{ skill.name }}</h3>
                <div class="sfia-{{ skill.sfia_level }} px-3 py-1 rounded-full text-xs">
                    {{ skill.get_sfia_level_display }}
                </div>
                <p class="text-sm text-gray-600 mt-4">{{ skill.description|truncatewords:20 }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

---

## 🐳 Docker Deployment

### Local Development with Docker

```bash
# Build and run
docker-compose up -d --build

# Check logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Production Deployment

#### Option 1: Azure App Service

```bash
# Login to Azure
az login

# Create resource group
az group create --name portfolio-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name portfolio-plan \
  --resource-group portfolio-rg \
  --sku B1 --is-linux

# Create web app
az webapp create \
  --name my-portfolio \
  --resource-group portfolio-rg \
  --plan portfolio-plan \
  --runtime "PYTHON:3.12"

# Configure settings
az webapp config appsettings set \
  --name my-portfolio \
  --resource-group portfolio-rg \
  --settings \
    SECRET_KEY="your-secret-key" \
    DEBUG="False" \
    ALLOWED_HOSTS="my-portfolio.azurewebsites.net"

# Deploy
az webapp up --name my-portfolio --resource-group portfolio-rg
```

#### Option 2: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add

# Deploy
railway up
```

#### Option 3: AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.12 portfolio

# Create environment
eb create portfolio-env

# Deploy
eb deploy
```

---

## 📊 Data Management

### Export Data to JSON

```bash
# Export all data
python manage.py export_json

# Files created in portfolio_project/data/:
# - profile.json
# - skills.json
# - projects.json
# - experience.json
# - certifications.json
# - blog.json
# - site.json
```

### Import Sample Data

Create fixtures for testing:

```bash
# Create fixture
python manage.py dumpdata core --indent 2 > fixtures/sample_data.json

# Load fixture
python manage.py loaddata fixtures/sample_data.json
```

---

## 🧪 Testing

### Unit Tests

Create `apps/core/tests.py`:

```python
from django.test import TestCase
from .models import Skill, SkillArea

class SkillModelTest(TestCase):
    def setUp(self):
        self.area = SkillArea.objects.create(name="Backend")
        self.skill = Skill.objects.create(
            area=self.area,
            name="Python",
            sfia_level="L3",
            description="Python development"
        )
    
    def test_skill_creation(self):
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(self.skill.sfia_level, "L3")
    
    def test_slug_generation(self):
        self.assertIsNotNone(self.skill.slug)
```

### Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=apps --cov-report=html

# View coverage
open htmlcov/index.html
```

---

## 📈 Performance Optimization

### 1. Database Optimization

```python
# In views, use select_related and prefetch_related
skills = Skill.objects.select_related('area').prefetch_related('projects')
```

### 2. Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def skills_view(request):
    # ...
```

### 3. Static Files Compression

```bash
# WhiteNoise handles this automatically
python manage.py collectstatic --noinput
```

### 4. Database Indexes

Already included in models:
- `created_at`, `updated_at` (TimeStampedModel)
- `slug` fields (unique indexes)
- `status` fields for filtering

---

## 🔒 Security Checklist

Before going to production:

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable SSL (`SECURE_SSL_REDIRECT=True`)
- [ ] Set secure cookie flags
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure CORS properly
- [ ] Set up rate limiting on contact form
- [ ] Enable CSRF protection
- [ ] Configure CSP headers
- [ ] Set up monitoring (Sentry)
- [ ] Enable logging
- [ ] Regular security updates

---

## 📚 Additional Resources

### Documentation
- Django: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- SFIA Framework: https://sfia-online.org/
- REST Framework: https://www.django-rest-framework.org/

### Tools
- PostgreSQL: https://www.postgresql.org/
- Docker: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/actions

---

## 🎯 Next Steps

1. **Immediate**:
   - Run setup script
   - Create Django project structure
   - Copy models, admin, settings
   - Run migrations

2. **Short-term** (Week 1):
   - Create views and templates
   - Implement home, about, skills pages
   - Add sample content via admin

3. **Medium-term** (Week 2-3):
   - Complete all pages (projects, blog, etc.)
   - Integrate existing HTML demo styling
   - Add contact form functionality
   - Test responsiveness

4. **Long-term** (Week 4+):
   - Docker deployment
   - Cloud hosting setup
   - SSL certificate
   - Domain configuration
   - SEO optimization
   - Analytics integration

---

## 💡 Pro Tips

1. **Use the Admin Heavily**: The Django admin is fully configured - use it to manage all content
2. **SFIA Evidence**: Link skills to projects/certs for automatic evidence tracking
3. **STAR Method**: Use the structured fields to showcase impact effectively
4. **JSON Export**: Use the export command to generate static JSON for the demo page
5. **Tailwind Classes**: Stick to core utility classes (no custom Tailwind compilation needed)
6. **Docker First**: Develop in Docker to match production environment

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up -d
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings
```

### Admin Styling Issues
```bash
# Make sure you've run collectstatic
python manage.py collectstatic --noinput
```

---

## 📞 Support

If you encounter issues:
1. Check the Django debug toolbar
2. Review logs in `logs/django_errors.log`
3. Enable SQL query logging in development
4. Check Docker logs: `docker-compose logs`

---

**Ready to build your portfolio! 🚀**