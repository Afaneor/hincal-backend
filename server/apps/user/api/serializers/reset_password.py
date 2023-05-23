from typing import Optional

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.user.models import User


class ResetPasswordRequestSerializer(serializers.Serializer):
    """Восстановление забытого пользователем пароля. Этап №1."""

    email = serializers.EmailField(required=True)

    user: Optional[User] = None

    def is_valid(self, raise_exception=False) -> bool:
        """Валидность email для восстановления пароля."""
        email = self.initial_data.get('email', None)
        self.check_email(email)
        return True

    def check_email(self, email) -> None:
        """Проверяем, что пользователь с такой почтой существует."""
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                {
                    'email': [_(
                        'Пользователя с таким email не существует',
                    )],
                },
            )


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """Успешное восстановление пароля пользователя. Этап №2."""

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        """Валидность username, email для восстановления пароля."""
        password1 = self.initial_data.get('password1')
        password2 = self.initial_data.get('password2')

        if password1 != password2:
            raise ValidationError(
                {'newPassword': [
                    _('Пароли должны совпадать! Проверьте корректность данных'),
                ]})
        try:
            validate_password(str(password1))
        except DjangoValidationError as exc:
            raise ValidationError(exc)
        return super().is_valid(raise_exception=raise_exception)
