# apps/core/admin.py
"""
Django Admin configuration for Portfolio application
Provides comprehensive content management interface
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Profile, SkillArea, Skill, Education, Experience,
    ProjectCategory, Project, ProjectImage,
    Certification, BlogSeries, BlogCategory, BlogTag, BlogPost,
    ContactMessage, SiteSettings
)


# ============================================================================
# ADMIN CUSTOMIZATION
# ============================================================================

class BaseAdmin(admin.ModelAdmin):
    """Base admin with common functionality"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self.model, 'created_at'):
            return qs.select_related()
        return qs


# ============================================================================
# PROFILE & RESUME
# ============================================================================

@admin.register(Profile)
class ProfileAdmin(BaseAdmin):
    list_display = ['name', 'job_title', 'email', 'is_active', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'job_title', 'email', 'phone', 'location')
        }),
        ('Bio & Summary', {
            'fields': ('bio', 'summary', 'meta_description')
        }),
        ('Profile Image', {
            'fields': ('profile_image', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'website_url'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.profile_image.url
            )
        return "No image"
    image_preview.short_description = "Current Image"


@admin.register(SkillArea)
class SkillAreaAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'skill_count', 'icon', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = "Skills"


@admin.register(Skill)
class SkillAdmin(BaseAdmin):
    list_display = [
        'name', 'area', 'sfia_badge', 'industry_level', 
        'sector', 'years_experience', 'is_featured'
    ]
    list_filter = ['sfia_level', 'industry_level', 'sector', 'is_featured', 'area']
    list_editable = ['is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = []
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('area', 'name', 'slug', 'description')
        }),
        ('SFIA Classification', {
            'fields': ('sfia_level', 'industry_level', 'sector', 'years_experience')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def sfia_badge(self, obj):
        colors = {
            'L1': '#10b981', 'L2': '#22c55e', 'L3': '#eab308',
            'L4': '#f97316', 'L5': '#3b82f6', 'L6': '#a855f7', 'L7': '#ef4444'
        }
        color = colors.get(obj.sfia_level, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; font-size: 11px;">{}</span>',
            color, obj.sfia_level
        )
    sfia_badge.short_description = "SFIA Level"


@admin.register(Education)
class EducationAdmin(BaseAdmin):
    list_display = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['institution', 'degree', 'field_of_study']
    filter_horizontal = ['skills']
    date_hierarchy = 'start_date'


# ============================================================================
# EXPERIENCE
# ============================================================================

@admin.register(Experience)
class ExperienceAdmin(BaseAdmin):
    list_display = ['role', 'company', 'duration_display', 'is_current', 'start_date']
    list_filter = ['is_current', 'start_date']
    search_fields = ['role', 'company', 'location']
    filter_horizontal = ['skills_used']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('role', 'company', 'location', 'company_url')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('STAR Method', {
            'fields': ('situation', 'task', 'action', 'result'),
            'description': 'Document experience using the STAR method'
        }),
        ('Skills & Display', {
            'fields': ('skills_used', 'order'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        try:
            return obj.duration
        except:
            return "-"
    duration_display.short_description = "Duration"


# ============================================================================
# PROJECTS
# ============================================================================

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'project_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = "Projects"


@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = [
        'title', 'category', 'duration_display', 
        'is_featured', 'is_ongoing', 'thumbnail_preview'
    ]
    list_filter = ['category', 'is_featured', 'is_ongoing', 'start_date']
    list_editable = ['is_featured']
    search_fields = ['title', 'situation', 'task', 'action', 'result']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['skills_demonstrated']
    date_hierarchy = 'start_date'
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_ongoing')
        }),
        ('STAR Method', {
            'fields': ('situation', 'task', 'action', 'result'),
            'description': 'Document project impact using the STAR method'
        }),
        ('Technical Details', {
            'fields': ('technologies', 'skills_demonstrated'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('thumbnail', 'featured_image'),
            'classes': ('collapse',)
        }),
        ('Links', {
            'fields': ('github_url', 'live_demo_url', 'case_study_url'),
            'classes': ('collapse',)
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def duration_display(self, obj):
        if obj.is_ongoing:
            return f"{obj.start_date.strftime('%b %Y')} - Present"
        elif obj.end_date:
            return f"{obj.start_date.strftime('%b %Y')} - {obj.end_date.strftime('%b %Y')}"
        return obj.start_date.strftime('%b %Y')
    duration_display.short_description = "Duration"
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 60px; max-height: 60px; '
                'border-radius: 4px;" />',
                obj.thumbnail.url
            )
        return "-"
    thumbnail_preview.short_description = "Thumbnail"


# ============================================================================
# CERTIFICATIONS
# ============================================================================

@admin.register(Certification)
class CertificationAdmin(BaseAdmin):
    list_display = [
        'title', 'cert_type', 'issuing_authority', 
        'issue_date', 'expiry_status', 'is_featured'
    ]
    list_filter = ['cert_type', 'is_featured', 'issue_date']
    list_editable = ['is_featured']
    search_fields = ['title', 'issuing_authority', 'credential_id']
    filter_horizontal = ['skills_validated']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'cert_type', 'issuing_authority', 'description')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Credentials', {
            'fields': ('credential_id', 'credential_url'),
            'classes': ('collapse',)
        }),
        ('Evidence', {
            'fields': ('certificate_file', 'badge_image'),
            'classes': ('collapse',)
        }),
        ('Skills & Display', {
            'fields': ('skills_validated', 'is_featured', 'icon_class', 'color_class')
        }),
    )
    
    def expiry_status(self, obj):
        if not obj.expiry_date:
            return format_html(
                '<span style="color: green;">✓ No Expiry</span>'
            )
        elif obj.is_expired:
            return format_html(
                '<span style="color: red;">✗ Expired</span>'
            )
        else:
            return format_html(
                '<span style="color: green;">✓ Valid</span>'
            )
    expiry_status.short_description = "Status"


# ============================================================================
# BLOG
# ============================================================================

@admin.register(BlogSeries)
class BlogSeriesAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'post_count', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(BlogCategory)
class BlogCategoryAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(BlogTag)
class BlogTagAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(BlogPost)
class BlogPostAdmin(BaseAdmin):
    list_display = [
        'title', 'status_badge', 'category', 'series',
        'published_date', 'view_count', 'is_featured'
    ]
    list_filter = ['status', 'category', 'series', 'is_featured', 'published_date']
    list_editable = ['is_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'series', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'published_date', 'reading_time')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    readonly_fields = []
    
    def status_badge(self, obj):
        colors = {
            'draft': '#9ca3af',
            'published': '#10b981',
            'archived': '#ef4444'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    actions = ['publish_posts', 'archive_posts']
    
    def publish_posts(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_date=timezone.now())
        self.message_user(request, f"{updated} post(s) published successfully.")
    publish_posts.short_description = "Publish selected posts"
    
    def archive_posts(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f"{updated} post(s) archived.")
    archive_posts.short_description = "Archive selected posts"


# ============================================================================
# CONTACT
# ============================================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(BaseAdmin):
    list_display = [
        'name', 'email', 'status_badge', 
        'created_at', 'subject_preview'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'message', 'created_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Metadata', {
            'fields': ('status', 'created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Admin Response', {
            'fields': ('admin_notes', 'replied_at')
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'new': '#3b82f6',
            'read': '#eab308',
            'replied': '#10b981',
            'archived': '#6b7280'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: 600; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def subject_preview(self, obj):
        return obj.subject[:50] + "..." if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = "Subject"
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f"{updated} message(s) marked as read.")
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_replied(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='replied', replied_at=timezone.now())
        self.message_user(request, f"{updated} message(s) marked as replied.")
    mark_as_replied.short_description = "Mark as replied"


# ============================================================================
# SITE SETTINGS
# ============================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(BaseAdmin):
    list_display = ['site_title', 'contact_email', 'is_active']
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'site_tagline', 'site_description')
        }),
        ('SEO', {
            'fields': ('meta_keywords', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Social Media', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Features', {
            'fields': ('enable_blog', 'enable_contact_form', 'maintenance_mode')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False


# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content Management"