# apps/core/models.py
"""
Core models for Portfolio Web Application
Implements SFIA-based skills and STAR method structure
"""
from datetime import timezone
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# ============================================================================
# RESUME MODULE
# ============================================================================

class Profile(TimeStampedModel):
    """Personal profile information"""
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    bio = models.TextField()
    summary = models.TextField(help_text="Brief professional summary")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200)
    
    # Profile image
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True
    )
    profile_banner = models.ImageField(
        upload_to='profile/banners/',
        blank=True,
        null=True
    )

    resume_pdf = models.FileField(
        upload_to='profile/resume/',
        blank=True,
        null=True
    )
    
    # Social links
    github_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Only one profile instance allowed
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one active profile
        if self.is_active:
            Profile.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class SkillArea(models.Model):
    """Skill category/area grouping"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class (e.g., fas fa-code)"
    )
    color = models.CharField(
        max_length=50,
        default='bg-blue-500',
        help_text="Tailwind color class (e.g., bg-blue-500)"
    )
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Skill Area"
        verbose_name_plural = "Skill Areas"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Skill(TimeStampedModel):
    """Individual skill with SFIA level classification"""
    
    # SFIA Level Choices (L1-L7)
    SFIA_LEVELS = [
        ('L1', 'L1 - Entry (Follow)'),
        ('L2', 'L2 - Foundation (Assist)'),
        ('L3', 'L3 - Practitioner (Apply)'),
        ('L4', 'L4 - Senior (Enable)'),
        ('L5', 'L5 - Lead (Ensure/Advise)'),
        ('L6', 'L6 - Principal (Initiate/Influence)'),
        ('L7', 'L7 - Expert (Set Strategy)'),
    ]
    
    # Industry-standard equivalents
    INDUSTRY_LEVELS = [
        ('entry', 'Entry'),
        ('foundation', 'Foundation'),
        ('practitioner', 'Practitioner'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
        ('principal', 'Principal'),
        ('expert', 'Expert'),
    ]
    
    SECTOR_CHOICES = [
        ('ecommerce', 'E-commerce'),
        ('edtech', 'EdTech'),
        ('banking', 'Banking'),
        ('devops', 'DevOps'),
        ('govtech', 'GovTech'),
        ('healthcare', 'Healthcare'),
        ('fintech', 'FinTech'),
        ('other', 'Other'),
    ]
    
    area = models.ForeignKey(
        SkillArea,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    skills = models.TextField(
        help_text="Specific technologies, tools, or methodologies",
        null=True,
        blank=True
    )
    slug = models.SlugField(unique=True, blank=True)
    
    # SFIA Classification
    sfia_level = models.CharField(
        max_length=2,
        choices=SFIA_LEVELS,
        default='L3'
    )
    industry_level = models.CharField(
        max_length=20,
        choices=INDUSTRY_LEVELS,
        default='practitioner'
    )
    
    # Context
    sector = models.CharField(
        max_length=20,
        choices=SECTOR_CHOICES,
        default='other'
    )
    description = models.TextField(
        help_text="Detailed description of skill proficiency"
    )
    
    # Years of experience (optional)
    years_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    # Tags for searching/filtering
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags for searching/filtering"
    )   

    # Display
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['area', 'order', 'name']
        unique_together = ['area', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.sfia_level})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.area.name}-{self.name}")
        super().save(*args, **kwargs)
    
    @property
    def evidence_items(self):
        """Get all evidence linking to this skill"""
        from core.models import Project
        from core.models import Certification
        
        evidence = []
        evidence.extend(self.projects.all())
        evidence.extend(self.certifications.all())
        evidence.extend(self.education_entries.all())
        return evidence


class Education(TimeStampedModel):
    """Education history"""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Link to skills
    skills = models.ManyToManyField(
        Skill,
        related_name='education_entries',
        blank=True
    )
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


# ============================================================================
# EXPERIENCE MODULE (STAR Method)
# ============================================================================

class Experience(TimeStampedModel):
    """Work experience with STAR method structure"""
    
    # Basic info
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to='experience/logos/',
        blank=True,
        null=True
    )
    company_website = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    # STAR Method fields
    situation = models.TextField(
        help_text="Context and challenge faced"
    )
    task = models.TextField(
        help_text="Responsibilities and objectives"
    )
    action = models.TextField(
        help_text="Steps taken and methods used"
    )
    result = models.TextField(
        help_text="Measurable outcomes and impact"
    )
    
    responsibilities = models.TextField(
        help_text="Key responsibilities and achievements",
        null=True,
        blank=True
    )
    technologies = models.TextField(
        help_text="Technologies and tools utilized",
        null=True,
        blank=True
    )
    achievements = models.TextField(
        help_text="Notable accomplishments",
        null=True,
        blank=True
    )
    # Additional details
    company_url = models.URLField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    # Link to skills
    skills_used = models.ManyToManyField(
        Skill,
        related_name='experiences',
        blank=True
    )
    
    class Meta:
        ordering = ['-start_date', 'order']
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
    
    def __str__(self):
        return f"{self.role} at {self.company}"
    
    @property
    def duration(self):
        """Calculate duration string"""
        end = self.end_date if self.end_date else timezone.now().date()
        delta = relativedelta(end, self.start_date)
        
        years = delta.years
        months = delta.months
        
        parts = []
        if years > 0:
            parts.append(f"{years} yr{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} mo{'s' if months > 1 else ''}")
        
        return " ".join(parts) if parts else "Less than 1 month"


# ============================================================================
# PROJECT MODULE (STAR Method)
# ============================================================================

class ProjectCategory(models.Model):
    """Project category/type"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(TimeStampedModel):
    """Project showcase with STAR method"""
    
    # Basic info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(
        help_text="Brief project summary for listings",
        null=True,
        blank=True,
        default=""
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects'
    )
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=200, blank=True)
    team_size = models.IntegerField(null=True, blank=True)
    client = models.CharField(max_length=200, null=True, blank=True)
    is_ongoing = models.BooleanField(default=False)
    github_link = models.URLField(null=True, blank=True)
    demo_link = models.URLField(null=True, blank=True)
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated tags for searching/filtering"
    )   

    # STAR Method fields
    situation = models.TextField(
        help_text="Problem context and business need"
    )
    task = models.TextField(
        help_text="Project objectives and deliverables"
    )
    action = models.TextField(
        help_text="Technical approach and implementation"
    )
    result = models.TextField(
        help_text="Business outcomes and metrics"
    )
    
    # Media
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/',
        blank=True,
        null=True
    )
    featured_image = models.ImageField(
        upload_to='projects/featured/',
        blank=True,
        null=True
    )
    
    # Links
    github_url = models.URLField(null=True, blank=True)
    live_demo_url = models.URLField(null=True, blank=True)
    case_study_url = models.URLField(null=True, blank=True)
    
    # Technologies (stored as JSON or M2M)
    technologies = models.JSONField(
        default=list,
        help_text="List of technologies used"
    )
    
    # Link to skills
    skills_demonstrated = models.ManyToManyField(
        Skill,
        related_name='projects',
        blank=True
    )
    
    # Display
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    """Additional project images"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


# ============================================================================
# CERTIFICATION MODULE
# ============================================================================

class Certification(TimeStampedModel):
    """Professional certifications and awards"""
    
    CERT_TYPES = [
        ('certification', 'Certification'),
        ('award', 'Award'),
        ('recognition', 'Recognition'),
        ('publication', 'Publication'),
    ]
    
    title = models.CharField(max_length=200)
    cert_type = models.CharField(
        max_length=20,
        choices=CERT_TYPES,
        default='certification'
    )
    issuing_authority = models.CharField(max_length=200)
    authority_website = models.URLField(null=True, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Credential details
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(null=True, blank=True)
    
    # Evidence
    certificate_file = models.FileField(
        upload_to='certifications/',
        blank=True,
        null=True
    )
    badge_image = models.ImageField(
        upload_to='certifications/badges/',
        blank=True,
        null=True
    )
    
    description = models.TextField(null=True, blank=True)
    
    # Link to skills
    skills_validated = models.ManyToManyField(
        Skill,
        related_name='certifications',
        blank=True
    )
    
    # Display
    is_featured = models.BooleanField(default=False)
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class"
    )
    color_class = models.CharField(
        max_length=50,
        default='bg-blue-500',
        help_text="Tailwind color class"
    )
    skills = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Comma-separated skills for searching/filtering"
    )
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.title} - {self.issuing_authority}"
    
    @property
    def is_expired(self):
        """Check if certification has expired"""
        if not self.expiry_date:
            return False
        from django.utils import timezone
        return self.expiry_date < timezone.now().date()


# ============================================================================
# BLOG MODULE
# ============================================================================

class BlogSeries(models.Model):
    """Blog series/collection grouping"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Blog Series"
        verbose_name_plural = "Blog Series"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogCategory(models.Model):
    """Blog post category"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    """Blog post tag"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    """Blog post with markdown support"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    
    # Organization
    series = models.ForeignKey(
        BlogSeries,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    
    # Content
    excerpt = models.TextField(
        max_length=300,
        help_text="Brief summary for listings"
    )
    content = models.TextField(help_text="Markdown content")
    
    # Media
    featured_image = models.ImageField(
        upload_to='blog/featured/',
        blank=True,
        null=True
    )
    
    # Publishing
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    published_date = models.DateTimeField(null=True, blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Reading stats
    reading_time = models.IntegerField(
        default=5,
        help_text="Estimated reading time in minutes"
    )
    view_count = models.IntegerField(default=0)
    
    # Display
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-publish date when status changes to published
        if self.status == 'published' and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_date


# ============================================================================
# CONTACT MODULE
# ============================================================================

class ContactMessage(TimeStampedModel):
    """Contact form submissions"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    # Metadata
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"


# ============================================================================
# SITE SETTINGS
# ============================================================================

class SiteSettings(models.Model):
    """Global site configuration (singleton)"""
    
    # Site info
    site_title = models.CharField(max_length=200, default="Portfolio")
    site_tagline = models.CharField(max_length=200, blank=True)
    site_description = models.TextField(null=True, blank=True)
    
    # SEO
    meta_keywords = models.CharField(max_length=500, blank=True)
    google_analytics_id = models.CharField(max_length=64, null=True, blank=True)
    
    # Contact
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20,  null=True, blank=True)
    
    # Social
    github_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    
    # Features
    enable_blog = models.BooleanField(default=True)
    enable_contact_form = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    
    # Singleton pattern
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one active instance
        if self.is_active:
            SiteSettings.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get the active site settings"""
        settings, created = cls.objects.get_or_create(
            is_active=True,
            defaults={
                'site_title': 'Portfolio',
                'contact_email': 'contact@example.com'
            }
        )
        return settings
