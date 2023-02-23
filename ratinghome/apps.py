from django.apps import AppConfig


class RatinghomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ratinghome'

    def ready(self):
        import ratinghome.signals  
