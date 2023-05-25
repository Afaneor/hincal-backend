from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Сериалайзер для авторизации пользователя."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    captcha_token = serializers.CharField(required=True)

    user: Optional[User] = None  # type: ignore

    def validate(self, attrs):
        """Пробуем авторизовать пользователя."""
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({
                'email': _('Пользователь с таким email не найден.'),
            })

        self.user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        return super().validate(attrs)  # type: ignore
