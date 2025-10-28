"""
Translation Circle App Configuration
"""

from django.apps import AppConfig


class TranslationConfig(AppConfig):
    """Configuration for translation circles sub-app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'circles.translation'
    verbose_name = 'Translation Circles'
