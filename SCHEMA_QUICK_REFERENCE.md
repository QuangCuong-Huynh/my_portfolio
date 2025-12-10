# Data Schema Quick Reference

## 📁 Files Created

1. **DATA_SCHEMAS.md** - Complete schema documentation
2. **templates_data.json** - Ready-to-use JSON templates
3. **This file** - Quick reference guide

---

## 🚀 Quick Start

### 1. View Existing Data

```bash
cd root
..\venv\Scripts\python.exe manage.py dumpdata core --indent=2 > current_data.json
```

### 2. Use Templates

Copy from `templates_data.json` and customize:

```json
{
  "profile_template": { ... },
  "skill_template": { ... },
  "experience_template": { ... }
}
```

### 3. Import Data

```bash
cd root
..\venv\Scripts\python.exe manage.py loaddata your_data.json
```

---

## 📊 Model Summary

| Model | Key Fields | Relations |
|-------|-----------|-----------|
| **Profile** | name, job_title, bio, email | None (Singleton) |
| **SkillArea** | name, slug, icon, color | → Skills |
| **Skill** | name, sfia_level, description | ← SkillArea, ↔ Many models |
| **Education** | institution, degree, dates | ↔ Skills |
| **Experience** | role, company, STAR fields | ↔ Skills |
| **Project** | title, STAR fields, technologies | ↔ Skills, ← Category |
| **Certification** | title, issuer, credentials | ↔ Skills |
| **BlogPost** | title, content, status | ← Series, Category, ↔ Tags |
| **ContactMessage** | name, email, message, status | None |
| **SiteSettings** | site_title, contact_email | None (Singleton) |

---

## 🎯 STAR Method Template

Use for **Experience** and **Project** models:

```json
"star": {
  "situation": "What was the context/challenge?",
  "task": "What were the objectives?",
  "action": "What steps did you take?",
  "result": "What were the measurable outcomes?"
}
```

---

## 📝 SFIA Levels Quick Reference

| Level | Title | Use When |
|-------|-------|----------|
| L1 | Entry (Follow) | Learning, following instructions |
| L2 | Foundation (Assist) | Assisting with supervision |
| L3 | Practitioner (Apply) | Working independently |
| L4 | Senior (Enable) | Guiding others |
| L5 | Lead (Ensure/Advise) | Leading teams, advising |
| L6 | Principal (Initiate/Influence) | Strategic influence |
| L7 | Expert (Set Strategy) | Industry leadership |

---

## 🔗 Common Relationships

### Skill Relationships

```
Skill ↔ Experience (M2M via skills_used)
Skill ↔ Project (M2M via skills_demonstrated)
Skill ↔ Certification (M2M via skills_validated)
Skill ↔ Education (M2M via skills)
```

### Category Relationships

```
SkillArea → Skill (FK)
ProjectCategory → Project (FK)
BlogCategory → BlogPost (FK)
BlogSeries → BlogPost (FK)
```

---

## 💾 Import/Export Commands

### Export All Data

```bash
cd root
..\venv\Scripts\python.exe manage.py dumpdata core --indent=2 > full_export.json
```

### Export Specific Models

```bash
# Skills only
..\venv\Scripts\python.exe manage.py dumpdata core.Skill core.SkillArea --indent=2 > skills.json

# Projects only
..\venv\Scripts\python.exe manage.py dumpdata core.Project core.ProjectCategory --indent=2 > projects.json

# Blog only
..\venv\Scripts\python.exe manage.py dumpdata core.BlogPost core.BlogCategory core.BlogTag --indent=2 > blog.json
```

### Import Data

```bash
..\venv\Scripts\python.exe manage.py loaddata data.json
```

### Clear Data (Careful!)

```bash
# Delete all data from a model
..\venv\Scripts\python.exe manage.py shell
>>> from core.models import Skill
>>> Skill.objects.all().delete()
```

---

## 🎨 Field Type Cheat Sheet

| Django Field | JSON Type | Example |
|--------------|-----------|---------|
| CharField | string | "Text" |
| TextField | string | "Long text..." |
| EmailField | string | "<user@example.com>" |
| URLField | string | "<https://example.com>" |
| DateField | string | "2025-01-15" |
| DateTimeField | string | "2025-01-15T10:30:00Z" |
| BooleanField | boolean | true |
| IntegerField | number | 42 |
| DecimalField | number | 3.85 |
| JSONField | object/array | {"key": "value"} |
| ImageField | string | "/media/image.jpg" |
| FileField | string | "/media/file.pdf" |

---

## ✅ Validation Checklist

Before importing data:

- [ ] All required fields present
- [ ] Dates in ISO 8601 format (YYYY-MM-DD)
- [ ] DateTimes in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- [ ] URLs are valid and complete
- [ ] Email addresses are valid
- [ ] Foreign key references exist
- [ ] Slugs are unique (or omit for auto-generation)
- [ ] SFIA levels are L1-L7
- [ ] JSON arrays are properly formatted
- [ ] No trailing commas in JSON

---

## 🔍 Admin Interface

Access at: <http://localhost:8000/admin/>

Create superuser:

```bash
cd root
..\venv\Scripts\python.exe manage.py createsuperuser
```

---

## 📚 Documentation Files

1. **DATA_SCHEMAS.md** - Full documentation with:
   - Complete model schemas
   - JSON templates
   - Field specifications
   - Validation rules
   - Best practices

2. **templates_data.json** - Ready-to-use templates for:
   - Profile
   - Skills
   - Experience
   - Projects
   - Certifications
   - Education
   - Blog Posts
   - Contact Messages
   - Site Settings

3. **root/data.json** - Sample data with real examples

4. **root/schemas/data_schema.json** - JSON Schema for validation

---

## 🛠️ Common Tasks

### Add a New Skill

```json
{
  "id": "skill-new",
  "area": "Cloud & DevOps",
  "name": "Kubernetes",
  "sfia_level": "L4",
  "description": "Container orchestration...",
  "tags": ["kubernetes", "docker", "cloud"]
}
```

### Add a New Project

```json
{
  "id": "project-new",
  "title": "My New Project",
  "slug": "my-new-project",
  "start_date": "2025-01-01",
  "star": {
    "situation": "...",
    "task": "...",
    "action": "...",
    "result": "..."
  },
  "technologies": ["Django", "React"]
}
```

### Update Profile

```bash
# Via admin: http://localhost:8000/admin/core/profile/
# Or via Django shell:
cd root
..\venv\Scripts\python.exe manage.py shell
>>> from core.models import Profile
>>> profile = Profile.objects.first()
>>> profile.job_title = "New Title"
>>> profile.save()
```

---

## 🎯 Best Practices

1. **Use STAR method** for Experience and Projects
2. **Tag consistently** (lowercase, hyphen-separated)
3. **Set SFIA levels** accurately for skills
4. **Include evidence** for skills (certifications, projects)
5. **Optimize images** before uploading
6. **Backup regularly** before bulk changes
7. **Test in admin** before JSON import
8. **Validate JSON** against schema

---

## 🆘 Troubleshooting

### Import Fails

- Check JSON syntax (use jsonlint.com)
- Verify all required fields present
- Ensure foreign keys exist
- Check for duplicate slugs

### Missing Relations

- Import in order: Areas → Skills → Everything else
- Use correct IDs for foreign keys
- Check M2M relationships are arrays

### Slug Conflicts

- Omit slug field for auto-generation
- Or ensure slugs are unique

---

## 📞 Quick Help

- **Full Documentation**: DATA_SCHEMAS.md
- **Templates**: templates_data.json
- **Sample Data**: root/data.json
- **Admin Panel**: <http://localhost:8000/admin/>
- **Django Docs**: <https://docs.djangoproject.com/>

---

**Last Updated:** 2025-12-11
