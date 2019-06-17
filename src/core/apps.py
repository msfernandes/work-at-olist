from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        if not settings.DISABLE_SIGNALS:
            from core import signals # noqa
