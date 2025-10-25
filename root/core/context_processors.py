"""
Custom context processors for template context
"""

from django.conf import settings
from core.models import SiteSettings


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
