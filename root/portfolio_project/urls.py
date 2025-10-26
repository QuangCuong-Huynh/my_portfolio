
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
from core.sitemaps import (
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
    path('', include('core.urls')),
    
    # API (optional)
    # path('api/v1/', include('core.api_urls')),
    
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
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'

