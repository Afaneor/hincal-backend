from typing import Optional

from django.contrib.auth.models import AnonymousUser

from server.apps.user.models import User


class ReportContext(object):
    """Формирование context для отчета."""

    def __int__(self, user: Optional[User, AnonymousUser], data: dict):
        """Инициализация переменных для работы."""
        self.user = user
        self.data = data

    def get_indicators(self):
        """Получение корректных показателей для формирования отчета."""


