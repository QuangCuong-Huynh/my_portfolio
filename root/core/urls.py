# apps/core/urls.py
"""
Core application URL patterns
"""

from django.urls import path
from core import views

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
    # path('api/data/profile/', views.profile_json, name='profile_json'),
    # path('api/data/skills/', views.skills_json, name='skills_json'),
    # path('api/data/projects/', views.projects_json, name='projects_json'),
    # path('api/data/experience/', views.experience_json, name='experience_json'),
    # path('api/data/certifications/', views.certifications_json, name='certifications_json'),
]

