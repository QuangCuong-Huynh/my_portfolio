from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

from .models import (
    Profile, Skill, SkillArea, Education, Experience,
    Project, ProjectCategory, Certification,
    BlogPost, BlogSeries, BlogCategory, BlogTag,
    ContactMessage, SiteSettings
)
from .forms import ContactForm


# ============================================================================
# HOME
# ============================================================================

class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['featured_skills'] = Skill.objects.filter(is_featured=True).select_related('area')[:6]
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        context['recent_posts'] = BlogPost.objects.filter(status='published')[:3]
        return context


# ============================================================================
# ABOUT / RESUME
# ============================================================================

class AboutView(TemplateView):
    """About/Resume page"""
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(is_active=True).first()
        context['skills'] = Skill.objects.select_related('area').all()
        context['education'] = Education.objects.all()
        context['certifications'] = Certification.objects.filter(is_featured=True)
        return context


class ResumeView(AboutView):
    """Resume page (print-friendly version)"""
    template_name = 'pages/resume.html'


def resume_download(request):
    """Generate and download PDF resume"""
    # TODO: Implement PDF generation with ReportLab or WeasyPrint
    return HttpResponse("PDF generation coming soon", content_type='text/plain')


# ============================================================================
# SKILLS
# ============================================================================

class SkillsListView(ListView):
    """Skills listing with filtering"""
    model = Skill
    template_name = 'pages/skills.html'
    context_object_name = 'skills'
    
    def get_queryset(self):
        qs = Skill.objects.select_related('area').prefetch_related(
            'projects', 'certifications', 'education_entries'
        )
        
        # Filter by SFIA level
        level = self.request.GET.get('level')
        if level:
            qs = qs.filter(sfia_level=level)
        
        # Filter by sector
        sector = self.request.GET.get('sector')
        if sector:
            qs = qs.filter(sector=sector)
        
        # Filter by area
        area = self.request.GET.get('area')
        if area:
            qs = qs.filter(area__slug=area)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_areas'] = SkillArea.objects.all()
        context['sfia_levels'] = Skill.SFIA_LEVELS
        context['sectors'] = Skill.SECTOR_CHOICES
        return context


class SkillDetailView(DetailView):
    """Individual skill detail"""
    model = Skill
    template_name = 'pages/skill_detail.html'
    context_object_name = 'skill'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.get_object()
        context['evidence'] = {
            'projects': skill.projects.all(),
            'certifications': skill.certifications.all(),
            'education': skill.education_entries.all(),
        }
        return context


# ============================================================================
# EXPERIENCE
# ============================================================================

class ExperienceListView(ListView):
    """Work experience listing"""
    model = Experience
    template_name = 'pages/experience.html'
    context_object_name = 'experiences'
    
    def get_queryset(self):
        return Experience.objects.prefetch_related('skills_used').all()


class ExperienceDetailView(DetailView):
    """Individual experience detail"""
    model = Experience
    template_name = 'pages/experience_detail.html'
    context_object_name = 'experience'


# ============================================================================
# PROJECTS
# ============================================================================

class ProjectsListView(ListView):
    """Projects listing with filtering"""
    model = Project
    template_name = 'pages/projects.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        qs = Project.objects.select_related('category').prefetch_related(
            'skills_demonstrated', 'images'
        )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        
        # Search
        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(situation__icontains=search) |
                Q(action__icontains=search)
            )
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        return context


class ProjectDetailView(DetailView):
    """Individual project detail"""
    model = Project
    template_name = 'pages/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self):
        return get_object_or_404(
            Project.objects.prefetch_related('skills_demonstrated', 'images'),
            slug=self.kwargs['slug']
        )


# ============================================================================
# BLOG
# ============================================================================

class BlogListView(ListView):
    """Blog posts listing"""
    model = BlogPost
    template_name = 'pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published'
        ).select_related('category', 'series').prefetch_related('tags')


class BlogSeriesView(DetailView):
    """Blog series with posts"""
    model = BlogSeries
    template_name = 'pages/blog_series.html'
    context_object_name = 'series'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.get_object()
        context['posts'] = series.posts.filter(status='published')
        return context


class BlogCategoryView(DetailView):
    """Blog category with posts"""
    model = BlogCategory
    template_name = 'pages/blog_category.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['posts'] = category.posts.filter(status='published')
        return context


class BlogTagView(DetailView):
    """Blog tag with posts"""
    model = BlogTag
    template_name = 'pages/blog_tag.html'
    context_object_name = 'tag'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context['posts'] = tag.posts.filter(status='published')
        return context


class BlogPostDetailView(DetailView):
    """Individual blog post"""
    model = BlogPost
    template_name = 'pages/blog_post.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.filter(status='published')
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj


# ============================================================================
# CERTIFICATIONS
# ============================================================================

class CertificationsListView(ListView):
    """Certifications listing"""
    model = Certification
    template_name = 'pages/certifications.html'
    context_object_name = 'certifications'
    
    def get_queryset(self):
        return Certification.objects.prefetch_related('skills_validated').all()


# ============================================================================
# CONTACT
# ============================================================================

class ContactView(FormView):
    """Contact form"""
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        # Save contact message
        contact = form.save(commit=False)
        contact.ip_address = self.get_client_ip()
        contact.user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:500]
        contact.save()
        
        messages.success(self.request, 'Thank you for your message! I will get back to you soon.')
        return super().form_valid(form)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


# ============================================================================
# DEMO / SPA
# ============================================================================

class DemoView(TemplateView):
    """Demo SPA page with JSON data"""
    template_name = 'pages/demo.html'


# ============================================================================
# JSON API ENDPOINTS (for demo page)
# ============================================================================

def profile_json(request):
    """Profile data as JSON"""
    profile = Profile.objects.filter(is_active=True).first()
    if not profile:
        return JsonResponse({})
    
    data = {
        'name': profile.name,
        'title': profile.job_title,
        'bio': profile.bio,
        'summary': profile.summary,
        'email': profile.email,
        'social': {
            'github': profile.github_url,
            'linkedin': profile.linkedin_url,
            'twitter': profile.twitter_url,
        }
    }
    return JsonResponse(data)


def skills_json(request):
    """Skills data as JSON"""
    skills = Skill.objects.select_related('area').all()
    data = []
    
    for skill in skills:
        data.append({
            'area': skill.area.name,
            'name': skill.name,
            'sfia': skill.sfia_level,
            'industry': skill.industry_level,
            'sector': skill.sector,
            'description': skill.description,
        })
    
    return JsonResponse(data, safe=False)


def projects_json(request):
    """Projects data as JSON"""
    projects = Project.objects.all()
    data = []
    
    for project in projects:
        data.append({
            'title': project.title,
            'technologies': project.technologies,
            'star': {
                'situation': project.situation,
                'task': project.task,
                'action': project.action,
                'result': project.result,
            }
        })
    
    return JsonResponse(data, safe=False)


def experience_json(request):
    """Experience data as JSON"""
    experiences = Experience.objects.all()
    data = []
    
    for exp in experiences:
        data.append({
            'role': exp.role,
            'company': exp.company,
            'star': {
                'situation': exp.situation,
                'task': exp.task,
                'action': exp.action,
                'result': exp.result,
            }
        })
    
    return JsonResponse(data, safe=False)


def certifications_json(request):
    """Certifications data as JSON"""
    certs = Certification.objects.all()
    data = []
    
    for cert in certs:
        data.append({
            'title': cert.title,
            'issuer': cert.issuing_authority,
            'date': cert.issue_date.isoformat(),
            'credential_id': cert.credential_id,
        })
    
    return JsonResponse(data, safe=False)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)


def custom_403(request, exception):
    """Custom 403 error page"""
    return render(request, 'errors/403.html', status=403)
