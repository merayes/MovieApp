from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'  # Uygulamanızın adı burada olmalı

    def ready(self):
        import profiles.signals  # Sinyalleri burada kaydediyoruz
