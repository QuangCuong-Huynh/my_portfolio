
# ==========================================================================
# apps/core/management/commands/export_json.py
"""
Management command to export portfolio data to JSON files
Usage: python manage.py export_json
"""

import json
from pathlib import Path
try:
    from django.core.management.base import BaseCommand
    from django.core.serializers.json import DjangoJSONEncoder
except Exception:
    # Lightweight fallbacks for editor/static analysis or non-Django environments.
    # When Django is available, the real classes will be used instead.
    class _DummyStyle:
        def SUCCESS(self, msg):
            return msg
        def WARNING(self, msg):
            return msg

    class _DummyStdout:
        def write(self, msg):
            # emulate BaseCommand.stdout.write
            print(msg)

    class BaseCommand:
        help = ''
        def __init__(self, *args, **kwargs):
            self.stdout = _DummyStdout()
            self.style = _DummyStyle()

    # Fallback JSON encoder
    DjangoJSONEncoder = json.JSONEncoder
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