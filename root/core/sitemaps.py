"""
Sitemap configuration for SEO
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from core.models import Skill, Project, BlogPost


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
