# apps/core/context_processors.py
"""
Custom context processors for template context
"""

from django.conf import settings
from apps.core.models import SiteSettings


def site_settings(request):
    """
    Add site settings to all template contexts
    """
    try:
        site_config = SiteSettings.get_settings()
    except:
        site_config = None
    
    return {
        'site_settings': site_config,
        'sfia_levels': settings.SFIA_LEVELS,
        'portfolio_settings': settings.PORTFOLIO_SETTINGS,
    }


# ==========================================================================
# portfolio_project/urls.py
"""
Main URL Configuration for Portfolio Web Application
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import (
    StaticViewSitemap, SkillSitemap, ProjectSitemap, 
    BlogPostSitemap
)

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'skills': SkillSitemap,
    'projects': ProjectSitemap,
    'blog': BlogPostSitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core pages
    path('', include('apps.core.urls')),
    
    # API (optional)
    path('api/v1/', include('apps.core.api_urls')),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    
    # Robots.txt
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    )),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Custom error handlers
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
handler403 = 'apps.core.views.custom_403'


# ==========================================================================
# apps/core/urls.py
"""
Core application URL patterns
"""

from django.urls import path
from apps.core import views

app_name = 'core'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # About/Resume
    path('about/', views.AboutView.as_view(), name='about'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('resume/download/', views.resume_download, name='resume_download'),
    
    # Skills
    path('skills/', views.SkillsListView.as_view(), name='skills'),
    path('skills/<slug:slug>/', views.SkillDetailView.as_view(), name='skill_detail'),
    
    # Experience
    path('experience/', views.ExperienceListView.as_view(), name='experience'),
    path('experience/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
    
    # Projects
    path('projects/', views.ProjectsListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/series/<slug:slug>/', views.BlogSeriesView.as_view(), name='blog_series'),
    path('blog/category/<slug:slug>/', views.BlogCategoryView.as_view(), name='blog_category'),
    path('blog/tag/<slug:slug>/', views.BlogTagView.as_view(), name='blog_tag'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog_post'),
    
    # Certifications
    path('certifications/', views.CertificationsListView.as_view(), name='certifications'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Demo/SPA
    path('demo/', views.DemoView.as_view(), name='demo'),
    
    # JSON API endpoints (for demo page)
    path('api/data/profile/', views.profile_json, name='profile_json'),
    path('api/data/skills/', views.skills_json, name='skills_json'),
    path('api/data/projects/', views.projects_json, name='projects_json'),
    path('api/data/experience/', views.experience_json, name='experience_json'),
    path('api/data/certifications/', views.certifications_json, name='certifications_json'),
]


# ==========================================================================
# apps/core/api_urls.py
"""
REST API URL patterns (optional)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.api_views import (
    SkillViewSet, ProjectViewSet, ExperienceViewSet,
    BlogPostViewSet, CertificationViewSet
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'blog', BlogPostViewSet, basename='blog')
router.register(r'certifications', CertificationViewSet, basename='certification')

urlpatterns = [
    path('', include(router.urls)),
]


# ==========================================================================
# apps/core/sitemaps.py
"""
Sitemap configuration for SEO
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.core.models import Skill, Project, BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'core:about', 'core:skills', 
                'core:projects', 'core:blog', 'core:certifications', 
                'core:contact']

    def location(self, item):
        return reverse(item)


class SkillSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Skill.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_featured=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return BlogPost.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('core:blog_post', args=[obj.slug])


# ==========================================================================
# apps/core/management/commands/export_json.py
"""
Management command to export portfolio data to JSON files
Usage: python manage.py export_json
"""

import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from apps.core.models import (
    Profile, Skill, Project, Experience, 
    Certification, BlogPost, SiteSettings
)


class Command(BaseCommand):
    help = 'Export portfolio data to JSON files'

    def handle(self, *args, **options):
        data_dir = Path('portfolio_project/data')
        data_dir.mkdir(exist_ok=True)
        
        self.stdout.write('Exporting portfolio data to JSON...')
        
        # Export profile
        self.export_profile(data_dir)
        
        # Export skills
        self.export_skills(data_dir)
        
        # Export projects
        self.export_projects(data_dir)
        
        # Export experience
        self.export_experience(data_dir)
        
        # Export certifications
        self.export_certifications(data_dir)
        
        # Export blog posts
        self.export_blog(data_dir)
        
        # Export site settings
        self.export_site_settings(data_dir)
        
        self.stdout.write(self.style.SUCCESS('✓ Export completed!'))
    
    def export_profile(self, data_dir):
        try:
            profile = Profile.objects.get(is_active=True)
            data = {
                'name': profile.name,
                'title': profile.job_title,
                'bio': profile.bio,
                'summary': profile.summary,
                'email': profile.email,
                'phone': profile.phone,
                'location': profile.location,
                'social': {
                    'github': profile.github_url,
                    'linkedin': profile.linkedin_url,
                    'twitter': profile.twitter_url,
                    'website': profile.website_url,
                }
            }
            
            with open(data_dir / 'profile.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write('  ✓ Exported profile.json')
        except Profile.DoesNotExist:
            self.stdout.write(self.style.WARNING('  ✗ No profile found'))
    
    def export_skills(self, data_dir):
        skills = Skill.objects.select_related('area').all()
        data = []
        
        for skill in skills:
            data.append({
                'area': skill.area.name,
                'name': skill.name,
                'slug': skill.slug,
                'sfia_level': skill.sfia_level,
                'industry_level': skill.industry_level,
                'sector': skill.sector,
                'description': skill.description,
                'years_experience': float(skill.years_experience) if skill.years_experience else None,
                'is_featured': skill.is_featured,
            })
        
        with open(data_dir / 'skills.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(f'  ✓ Exported {len(data)} skills')
    
    def export_projects(self, data_dir):
        projects = Project.objects.all()
        data = []
        
        for project in projects:
            data.append({
                'title': project.title,
                'slug': project.slug,
                'category': project.category.name if project.category else None,
                'start_date': project.start_date.isoformat(),
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'is_ongoing': project.is_ongoing,
                'star': {
                    'situation': project.situation,
                    'task': project.task,
                    'action': project.action,
                    'result': project.result,
                },
                'technologies': project.technologies,
                'github_url': project.github_url,
                'live_demo_url': project.live_demo_url,
                'is_featured': project.is_featured,
            })
        
        with open(data_dir / 'projects.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(f'  ✓ Exported {len(data)} projects')
    
    def export_experience(self, data_dir):
        experiences = Experience.objects.all()
        data = []
        
        for exp in experiences:
            data.append({
                'role': exp.role,
                'company': exp.company,
                'location': exp.location,
                'start_date': exp.start_date.isoformat(),
                'end_date': exp.end_date.isoformat() if exp.end_date else None,
                'is_current': exp.is_current,
                'star': {
                    'situation': exp.situation,
                    'task': exp.task,
                    'action': exp.action,
                    'result': exp.result,
                },
                'company_url': exp.company_url,
            })
        
        with open(data_dir / 'experience.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(f'  ✓ Exported {len(data)} experiences')
    
    def export_certifications(self, data_dir):
        certs = Certification.objects.all()
        data = []
        
        for cert in certs:
            data.append({
                'title': cert.title,
                'type': cert.cert_type,
                'issuing_authority': cert.issuing_authority,
                'issue_date': cert.issue_date.isoformat(),
                'expiry_date': cert.expiry_date.isoformat() if cert.expiry_date else None,
                'credential_id': cert.credential_id,
                'credential_url': cert.credential_url,
                'icon_class': cert.icon_class,
                'color_class': cert.color_class,
                'is_featured': cert.is_featured,
            })
        
        with open(data_dir / 'certifications.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(f'  ✓ Exported {len(data)} certifications')
    
    def export_blog(self, data_dir):
        posts = BlogPost.objects.filter(status='published')
        data = []
        
        for post in posts:
            data.append({
                'title': post.title,
                'slug': post.slug,
                'series': post.series.name if post.series else None,
                'category': post.category.name if post.category else None,
                'excerpt': post.excerpt,
                'content': post.content,
                'published_date': post.published_date.isoformat() if post.published_date else None,
                'reading_time': post.reading_time,
                'is_featured': post.is_featured,
            })
        
        with open(data_dir / 'blog.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(f'  ✓ Exported {len(data)} blog posts')
    
    def export_site_settings(self, data_dir):
        try:
            settings = SiteSettings.get_settings()
            data = {
                'site_title': settings.site_title,
                'site_tagline': settings.site_tagline,
                'site_description': settings.site_description,
                'contact_email': settings.contact_email,
                'contact_phone': settings.contact_phone,
                'social': {
                    'github': settings.github_url,
                    'linkedin': settings.linkedin_url,
                    'twitter': settings.twitter_url,
                },
                'features': {
                    'enable_blog': settings.enable_blog,
                    'enable_contact_form': settings.enable_contact_form,
                }
            }
            
            with open(data_dir / 'site.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write('  ✓ Exported site.json')
        except:
            self.stdout.write(self.style.WARNING('  ✗ No site settings found'))