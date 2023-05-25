from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """Регистрация пользователя."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    inn = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False) -> bool:
        """Проверка валидности данных для регистрации пользователя."""
        self._validate_email()
        self._validate_password()

        return super().is_valid(raise_exception)

    def _validate_email(self) -> None:
        if User.objects.filter(email=self.initial_data['email']).exists():
            initial_email = self.initial_data['email']
            raise ValidationError({
                'email': [_(
                    f'Пользователь с email {initial_email} ' +
                    'уже существует, укажите другой email или ' +
                    'попробуйте восстановить пароль.',
                )],
            })

    def _validate_password(self):  # noqa: WPS238
        password1 = self.initial_data.get('password1', None)
        password2 = self.initial_data.get('password2', None)

        if not password1:
            raise ValidationError(
                {'password1': [_('Необходимо указать пароль')]},
            )

        if not password2:
            raise ValidationError(
                {'password2': [_('Необходимо указать пароль два раза')]},
            )

        if password1 != password2:
            raise ValidationError(
                {'password': [_('Оба пароля должны совпадать')]},
            )

        try:
            validate_password(str(password1))
        except DjangoValidationError as exc:
            raise ValidationError(exc)


class ConfirmEmailRequestSerializer(serializers.Serializer):
    """Сериализатор отправки сообщения подтверждения регистрации."""

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
            raise NotFound(_('Пользователь не найден'))

        if self.user.is_active:
            raise ValidationError(
                {'email': [_('Пользователь с указанным email уже активен')]},
            )
        return self.user


class ConfirmEmailProcessSerializer(serializers.Serializer):
    """Успешное подтверждение регистрации.

    Сериализитор не несет смысловой нагрузки, но нужен для того, чтобы
    не удалось случайно активировать аккаунт у пользователя.
    """

    is_active = serializers.BooleanField(required=True)
