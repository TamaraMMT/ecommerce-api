from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    """
    Signals for automatic UserProfile creation on user creation.
    """

    def ready(self, *args, **kwargs) -> None:
        import user.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready
