# Portfolio Data Schemas & Format Templates

## 📋 Table of Contents

- [Overview](#overview)
- [Database Models](#database-models)
- [JSON Data Format](#json-data-format)
- [Field Specifications](#field-specifications)
- [Template Examples](#template-examples)
- [Validation Rules](#validation-rules)

---

## Overview

This document provides comprehensive data schemas for the Django Portfolio Application, including:

- **Django ORM Models** - Database structure
- **JSON Data Format** - Import/export templates
- **Field Specifications** - Data types, constraints, and validation
- **Template Examples** - Ready-to-use data templates

---

## Database Models

### Model Hierarchy

```
TimeStampedModel (Abstract Base)
├── Profile
├── Skill
│   └── SkillArea (FK)
├── Education
│   └── Skills (M2M)
├── Experience
│   └── Skills (M2M)
├── Project
│   ├── ProjectCategory (FK)
│   ├── Skills (M2M)
│   └── ProjectImage (Related)
├── Certification
│   └── Skills (M2M)
├── BlogPost
│   ├── BlogSeries (FK)
│   ├── BlogCategory (FK)
│   └── BlogTag (M2M)
├── ContactMessage
└── SiteSettings (Singleton)
```

---

## 1. Profile Model

### Django Model Schema

```python
class Profile(TimeStampedModel):
    # Basic Info
    name = CharField(max_length=200)
    job_title = CharField(max_length=200)
    bio = TextField()
    summary = TextField()
    email = EmailField()
    phone = CharField(max_length=20, blank=True)
    location = CharField(max_length=200)
    
    # Media
    profile_image = ImageField(upload_to='profile/', blank=True, null=True)
    profile_banner = ImageField(upload_to='profile/banners/', blank=True, null=True)
    resume_pdf = FileField(upload_to='profile/resume/', blank=True, null=True)
    
    # Social Links
    github_url = URLField(null=True, blank=True)
    linkedin_url = URLField(null=True, blank=True)
    twitter_url = URLField(null=True, blank=True)
    website_url = URLField(null=True, blank=True)
    
    # SEO
    meta_description = CharField(max_length=160, blank=True)
    
    # Status
    is_active = BooleanField(default=True)  # Singleton pattern
```

### JSON Template

```json
{
  "id": "profile-001",
  "name": "John Doe",
  "job_title": "Full-Stack Developer | Cloud Architect",
  "bio": "Experienced software engineer specializing in cloud architecture...",
  "summary": "Building scalable systems with modern technologies.",
  "location": "San Francisco, CA",
  "email": "john@example.com",
  "phone": "+1-555-0100",
  "avatar": "/assets/images/avatar.jpg",
  "banner": "/assets/images/banner.jpg",
  "resume_pdf": "/assets/resume.pdf",
  "social": {
    "github": "https://github.com/johndoe",
    "linkedin": "https://linkedin.com/in/johndoe",
    "twitter": "https://twitter.com/johndoe",
    "website": "https://johndoe.dev"
  },
  "meta_description": "Professional portfolio of John Doe - Full-Stack Developer",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-12-11T00:00:00Z"
}
```

---

## 2. Skill Model

### Django Model Schema

```python
class SkillArea(models.Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True, blank=True)
    description = TextField(null=True, blank=True)
    icon = CharField(max_length=50, blank=True)  # Font Awesome class
    color = CharField(max_length=50, default='bg-blue-500')  # Tailwind class
    order = IntegerField(default=0)

class Skill(TimeStampedModel):
    # Classification
    area = ForeignKey(SkillArea, on_delete=CASCADE, related_name='skills')
    name = CharField(max_length=100)
    skills = TextField(help_text="Specific technologies", null=True, blank=True)
    slug = SlugField(unique=True, blank=True)
    
    # SFIA Levels: L1-L7
    sfia_level = CharField(max_length=2, choices=SFIA_LEVELS, default='L3')
    industry_level = CharField(max_length=20, choices=INDUSTRY_LEVELS)
    
    # Context
    sector = CharField(max_length=20, choices=SECTOR_CHOICES, default='other')
    description = TextField()
    years_experience = DecimalField(max_digits=4, decimal_places=1, null=True)
    
    # Metadata
    tags = CharField(max_length=200, blank=True)
    is_featured = BooleanField(default=False)
    order = IntegerField(default=0)
```

### SFIA Level Reference

| Level | Title | Description |
|-------|-------|-------------|
| L1 | Entry (Follow) | Follow instructions under close supervision |
| L2 | Foundation (Assist) | Assist with defined tasks with limited supervision |
| L3 | Practitioner (Apply) | Apply knowledge independently |
| L4 | Senior (Enable) | Enable others through guidance |
| L5 | Lead (Ensure/Advise) | Ensure delivery and advise on complex matters |
| L6 | Principal (Initiate/Influence) | Initiate strategy and influence direction |
| L7 | Expert (Set Strategy) | Set organizational strategy |

### JSON Template

```json
{
  "id": "skill-001",
  "area": "Cloud & DevOps",
  "name": "Cloud Architecture & Infrastructure as Code",
  "skills": ["Azure (CAF, Bicep)", "AWS (EC2, Lambda)", "Terraform", "Kubernetes"],
  "sfia_level": "L5",
  "industry_level": "Lead Architect",
  "proficiency": "expert",
  "sector": "Enterprise & Public Cloud",
  "description": "Designs enterprise-grade multi-cloud architectures with IaC-first principles...",
  "years_experience": 7.0,
  "last_used": "2025",
  "evidence": [
    {
      "type": "certification",
      "title": "AWS Certified Solutions Architect – Professional",
      "url": "/certifications/aws-sap",
      "date": "2025-03-15"
    }
  ],
  "tags": ["cloud", "devops", "terraform", "azure", "aws"],
  "featured": true,
  "order": 1
}
```

---

## 3. Experience Model (STAR Method)

### Django Model Schema

```python
class Experience(TimeStampedModel):
    # Basic Info
    role = CharField(max_length=200)
    company = CharField(max_length=200)
    company_logo = ImageField(upload_to='experience/logos/', blank=True, null=True)
    company_website = URLField(null=True, blank=True)
    location = CharField(max_length=200)
    employment_type = CharField(max_length=100, blank=True)
    start_date = DateField()
    end_date = DateField(null=True, blank=True)
    is_current = BooleanField(default=False)
    
    # STAR Method
    situation = TextField(help_text="Context and challenge faced")
    task = TextField(help_text="Responsibilities and objectives")
    action = TextField(help_text="Steps taken and methods used")
    result = TextField(help_text="Measurable outcomes and impact")
    
    # Additional
    responsibilities = TextField(null=True, blank=True)
    technologies = TextField(null=True, blank=True)
    achievements = TextField(null=True, blank=True)
    company_url = URLField(null=True, blank=True)
    order = IntegerField(default=0)
    
    # Relations
    skills_used = ManyToManyField(Skill, related_name='experiences', blank=True)
```

### JSON Template

```json
{
  "id": "exp-001",
  "role": "Senior Cloud Architect",
  "company": "TechCorp Global",
  "company_logo": "/assets/images/companies/techcorp.png",
  "company_website": "https://techcorp.com",
  "location": "San Francisco, CA (Hybrid)",
  "employment_type": "Full-time",
  "start_date": "2022-01-01",
  "end_date": null,
  "current": true,
  "period": "2022 – Present",
  "star": {
    "situation": "The enterprise faced operational fragmentation across multi-cloud platforms...",
    "task": "Architect a unified, secure, and compliant multi-cloud foundation...",
    "action": "Designed cloud governance blueprints with IaC using Terraform and Bicep...",
    "result": "Reduced audit preparation time by 70%, achieved continuous compliance..."
  },
  "responsibilities": [
    "Design and govern enterprise multi-cloud architectures",
    "Implement Zero Trust security models",
    "Lead DevSecOps transformation"
  ],
  "technologies": ["Azure CAF", "Terraform", "Kubernetes", "GitLab CI/CD"],
  "achievements": [
    "70% faster compliance audits",
    "99.95% uptime reliability"
  ],
  "skills_used": ["skill-001", "skill-002"],
  "featured": true,
  "order": 1
}
```

---

## 4. Project Model (STAR Method)

### Django Model Schema

```python
class ProjectCategory(models.Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True, blank=True)
    description = TextField(null=True, blank=True)

class Project(TimeStampedModel):
    # Basic Info
    title = CharField(max_length=200)
    slug = SlugField(unique=True, blank=True)
    summary = TextField(null=True, blank=True)
    category = ForeignKey(ProjectCategory, on_delete=SET_NULL, null=True)
    
    # Timeline
    start_date = DateField()
    end_date = DateField(null=True, blank=True)
    role = CharField(max_length=200, blank=True)
    team_size = IntegerField(null=True, blank=True)
    client = CharField(max_length=200, null=True, blank=True)
    is_ongoing = BooleanField(default=False)
    
    # STAR Method
    situation = TextField(help_text="Problem context and business need")
    task = TextField(help_text="Project objectives and deliverables")
    action = TextField(help_text="Technical approach and implementation")
    result = TextField(help_text="Business outcomes and metrics")
    
    # Media
    thumbnail = ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    featured_image = ImageField(upload_to='projects/featured/', blank=True, null=True)
    
    # Links
    github_url = URLField(null=True, blank=True)
    live_demo_url = URLField(null=True, blank=True)
    case_study_url = URLField(null=True, blank=True)
    
    # Technologies (JSON array)
    technologies = JSONField(default=list)
    tags = CharField(max_length=200, blank=True)
    
    # Relations
    skills_demonstrated = ManyToManyField(Skill, related_name='projects', blank=True)
    
    # Display
    is_featured = BooleanField(default=False)
    order = IntegerField(default=0)
```

### JSON Template

```json
{
  "id": "project-001",
  "slug": "django-mvvm-framework",
  "title": "Django MVVM Enterprise Framework",
  "summary": "A modular full-stack MVVM Django architecture...",
  "description": "Designed a scalable Django MVVM framework for enterprise applications...",
  "thumbnail": "/assets/images/projects/django-mvvm-thumb.jpg",
  "images": [
    "/assets/images/projects/django-mvvm-1.jpg",
    "/assets/images/projects/django-mvvm-2.jpg"
  ],
  "category": "Software Architecture",
  "status": "active",
  "start_date": "2025-09-01",
  "end_date": null,
  "period": "2025 – Present",
  "role": "Lead Developer & Architect",
  "team_size": 1,
  "client": null,
  "star": {
    "situation": "Needed a reusable full-stack scaffold to accelerate Django project setup...",
    "task": "Design an enterprise-ready Django architecture template...",
    "action": "Implemented base apps structure, automated environment setup scripts...",
    "result": "Reduced new project setup time from 2 days to under 2 hours..."
  },
  "technologies": ["Django", "SQLite", "React", "Docker", "Pytest", "GitLab CI/CD"],
  "links": {
    "github": "https://github.com/user/django-mvvm-framework",
    "demo": null,
    "website": null
  },
  "tags": ["django", "mvvm", "devsecops", "architecture"],
  "skills_demonstrated": ["skill-003"],
  "featured": true,
  "order": 1,
  "metrics": {
    "setup_time_reduction": "90%",
    "test_coverage": "85%"
  }
}
```

---

## 5. Certification Model

### Django Model Schema

```python
class Certification(TimeStampedModel):
    CERT_TYPES = [
        ('certification', 'Certification'),
        ('award', 'Award'),
        ('recognition', 'Recognition'),
        ('publication', 'Publication'),
    ]
    
    title = CharField(max_length=200)
    cert_type = CharField(max_length=20, choices=CERT_TYPES, default='certification')
    issuing_authority = CharField(max_length=200)
    authority_website = URLField(null=True, blank=True)
    issue_date = DateField()
    expiry_date = DateField(null=True, blank=True)
    
    # Credentials
    credential_id = CharField(max_length=200, blank=True)
    credential_url = URLField(null=True, blank=True)
    
    # Evidence
    certificate_file = FileField(upload_to='certifications/', blank=True, null=True)
    badge_image = ImageField(upload_to='certifications/badges/', blank=True, null=True)
    description = TextField(null=True, blank=True)
    
    # Relations
    skills_validated = ManyToManyField(Skill, related_name='certifications', blank=True)
    
    # Display
    is_featured = BooleanField(default=False)
    icon_class = CharField(max_length=50, blank=True)
    color_class = CharField(max_length=50, default='bg-blue-500')
    skills = CharField(max_length=200, blank=True)
```

### JSON Template

```json
{
  "id": "cert-001",
  "title": "AWS Certified Solutions Architect – Professional",
  "cert_type": "certification",
  "issuer": "Amazon Web Services",
  "authority_website": "https://aws.amazon.com/certification/",
  "issue_date": "2025-03-15",
  "expiry_date": "2028-03-15",
  "credential_id": "AWS-SAP-2025-1987",
  "credential_url": "https://www.credly.com/badges/example",
  "evidence_link": "/assets/certs/aws-sap.pdf",
  "logo": "/assets/images/certs/aws.png",
  "icon": "fas fa-cloud",
  "color": "bg-orange-500",
  "status": "active",
  "featured": true,
  "order": 1,
  "skills": ["cloud-architecture", "aws", "infrastructure", "devops"],
  "description": "Validates expert-level ability to design and deploy distributed systems..."
}
```

---

## 6. Education Model

### Django Model Schema

```python
class Education(TimeStampedModel):
    institution = CharField(max_length=200)
    degree = CharField(max_length=200)
    field_of_study = CharField(max_length=200)
    start_date = DateField()
    end_date = DateField(null=True, blank=True)
    is_current = BooleanField(default=False)
    description = TextField(null=True, blank=True)
    gpa = DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Relations
    skills = ManyToManyField(Skill, related_name='education_entries', blank=True)
```

### JSON Template

```json
{
  "id": "edu-001",
  "institution": "Stanford University",
  "degree": "Master of Science",
  "field_of_study": "Computer Science",
  "start_date": "2018-09-01",
  "end_date": "2020-06-15",
  "is_current": false,
  "description": "Specialized in distributed systems and cloud computing...",
  "gpa": 3.85,
  "skills": ["skill-001", "skill-003"],
  "achievements": [
    "Dean's List (4 semesters)",
    "Published research on container orchestration"
  ]
}
```

---

## 7. Blog Post Model

### Django Model Schema

```python
class BlogSeries(models.Model):
    name = CharField(max_length=200)
    slug = SlugField(unique=True, blank=True)
    description = TextField()
    order = IntegerField(default=0)

class BlogCategory(models.Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True, blank=True)
    description = TextField(null=True, blank=True)

class BlogTag(models.Model):
    name = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True, blank=True)

class BlogPost(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = CharField(max_length=200)
    slug = SlugField(unique=True, blank=True)
    series = ForeignKey(BlogSeries, on_delete=SET_NULL, null=True, blank=True)
    category = ForeignKey(BlogCategory, on_delete=SET_NULL, null=True)
    tags = ManyToManyField(BlogTag, blank=True)
    
    # Content
    excerpt = TextField(max_length=300)
    content = TextField(help_text="Markdown content")
    featured_image = ImageField(upload_to='blog/featured/', blank=True, null=True)
    
    # Publishing
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = DateTimeField(null=True, blank=True)
    
    # SEO
    meta_description = CharField(max_length=160, blank=True)
    meta_keywords = CharField(max_length=200, blank=True)
    
    # Stats
    reading_time = IntegerField(default=5)
    view_count = IntegerField(default=0)
    
    # Display
    is_featured = BooleanField(default=False)
    order = IntegerField(default=0)
```

### JSON Template

```json
{
  "id": "blog-001",
  "slug": "building-zero-trust-architecture",
  "title": "Building Zero Trust Architecture on Azure",
  "excerpt": "A comprehensive guide to implementing Zero Trust principles...",
  "content": "# Introduction\n\nZero Trust Architecture (ZTA) is...",
  "featured_image": "/assets/images/blog/zero-trust.jpg",
  "series": "Cloud Security Series",
  "category": "Security",
  "tags": ["zero-trust", "azure", "security", "cloud"],
  "status": "published",
  "published_date": "2025-11-15T10:00:00Z",
  "meta_description": "Learn how to implement Zero Trust Architecture on Azure...",
  "meta_keywords": "zero trust, azure, security, cloud architecture",
  "reading_time": 12,
  "view_count": 1547,
  "featured": true,
  "order": 1
}
```

---

## 8. Contact Message Model

### Django Model Schema

```python
class ContactMessage(TimeStampedModel):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = CharField(max_length=200)
    email = EmailField()
    subject = CharField(max_length=200, blank=True)
    message = TextField()
    
    # Metadata
    status = CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    ip_address = GenericIPAddressField(null=True, blank=True)
    user_agent = CharField(max_length=500, blank=True)
    
    # Admin
    admin_notes = TextField(null=True, blank=True)
    replied_at = DateTimeField(null=True, blank=True)
```

---

## 9. Site Settings Model (Singleton)

### Django Model Schema

```python
class SiteSettings(models.Model):
    # Site Info
    site_title = CharField(max_length=200, default="Portfolio")
    site_tagline = CharField(max_length=200, blank=True)
    site_description = TextField(null=True, blank=True)
    
    # SEO
    meta_keywords = CharField(max_length=500, blank=True)
    google_analytics_id = CharField(max_length=64, null=True, blank=True)
    
    # Contact
    contact_email = EmailField()
    contact_phone = CharField(max_length=20, null=True, blank=True)
    
    # Social
    github_url = URLField(null=True, blank=True)
    linkedin_url = URLField(null=True, blank=True)
    twitter_url = URLField(null=True, blank=True)
    
    # Features
    enable_blog = BooleanField(default=True)
    enable_contact_form = BooleanField(default=True)
    maintenance_mode = BooleanField(default=False)
    
    # Singleton
    is_active = BooleanField(default=True)
```

---

## Complete JSON Data Structure

### Full Portfolio Data Template

```json
{
  "site": {
    "metadata": {
      "title": "Portfolio Title",
      "author": "Your Name",
      "description": "Portfolio description",
      "keywords": ["keyword1", "keyword2"],
      "language": "en",
      "theme": "light",
      "version": "1.0.0"
    },
    "social": {
      "github": "https://github.com/username",
      "linkedin": "https://linkedin.com/in/username",
      "twitter": "https://twitter.com/username",
      "email": "contact@example.com",
      "website": "https://example.com"
    },
    "navigation": [
      {"label": "Home", "path": "/", "icon": "fas fa-home"},
      {"label": "Skills", "path": "/skills", "icon": "fas fa-code"},
      {"label": "Projects", "path": "/projects", "icon": "fas fa-folder-open"}
    ]
  },
  "profiles": [...],
  "skills": [...],
  "experience": [...],
  "projects": [...],
  "certifications": [...],
  "education": [...],
  "blog_posts": [...]
}
```

---

## Field Type Reference

### Common Field Types

| Django Type | JSON Type | Description | Example |
|-------------|-----------|-------------|---------|
| CharField | string | Text field with max length | "John Doe" |
| TextField | string | Unlimited text | "Long description..." |
| EmailField | string | Email address | "<user@example.com>" |
| URLField | string | URL | "<https://example.com>" |
| DateField | string | ISO date | "2025-01-15" |
| DateTimeField | string | ISO datetime | "2025-01-15T10:30:00Z" |
| BooleanField | boolean | True/False | true |
| IntegerField | number | Integer | 42 |
| DecimalField | number | Decimal | 3.85 |
| JSONField | object/array | JSON data | {"key": "value"} |
| ImageField | string | Image path | "/media/image.jpg" |
| FileField | string | File path | "/media/file.pdf" |

---

## Validation Rules

### Required Fields by Model

**Profile:**

- name, job_title, bio, summary, email, location

**Skill:**

- area, name, sfia_level, description

**Experience:**

- role, company, location, start_date, situation, task, action, result

**Project:**

- title, start_date, situation, task, action, result

**Certification:**

- title, issuing_authority, issue_date

**BlogPost:**

- title, excerpt, content, status

---

## Import/Export Commands

### Export Data to JSON

```bash
cd root
..\venv\Scripts\python.exe manage.py dumpdata core --indent=2 > data_export.json
```

### Import Data from JSON

```bash
cd root
..\venv\Scripts\python.exe manage.py loaddata data.json
```

### Export Specific Models

```bash
# Export only skills
..\venv\Scripts\python.exe manage.py dumpdata core.Skill --indent=2 > skills.json

# Export only projects
..\venv\Scripts\python.exe manage.py dumpdata core.Project --indent=2 > projects.json
```

---

## Schema Validation

### JSON Schema File

Location: `root/schemas/data_schema.json`

Use for validating JSON data before import.

---

## Best Practices

1. **Always use ISO 8601 format** for dates and datetimes
2. **Slugs are auto-generated** from titles/names if not provided
3. **Use STAR method** for Experience and Project descriptions
4. **Tag consistently** using lowercase, hyphen-separated values
5. **Maintain relationships** by referencing IDs correctly
6. **Validate JSON** against schema before importing
7. **Backup data** before bulk imports

---

## Additional Resources

- Django Models: `root/core/models.py`
- JSON Schema: `root/schemas/data_schema.json`
- Sample Data: `root/data.json`
- Admin Interface: <http://localhost:8000/admin/>

---

**Last Updated:** 2025-12-11
**Version:** 1.0.0
