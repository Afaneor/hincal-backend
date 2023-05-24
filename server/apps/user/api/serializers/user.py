from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.apps.cicada.models import Company, CompanyUsers
from server.apps.cicada.services.enums import CompanyUserRole
from server.apps.notification.tasks import (
    notify_user_about_consolidation_company,
)
from server.apps.services.absolute_backend_endpoint import (
    absolute_backend_endpoint,
)
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.models import Profile

User = get_user_model()


class BaseInfoUserWithProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя и профиля.

    Используется в других сериалайзерах.
    """

    avatar = serializers.SerializerMethodField()

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'avatar',
        )

    def get_avatar(self, user) -> str:
        """Получение аватара из профиля."""
        avatar = user.profile.avatar
        request = self.context.get('request')
        return request.build_absolute_uri(avatar.url) if avatar else ''


class BaseInfoUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя. Используется в других сериалайзерах."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'middle_name',
        )


class UserSerializer(ModelSerializerWithPermission):
    """Детальная информация о пользователе."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'is_active',
            'permission_rules',
        )


class CreateUserSerializer(serializers.Serializer):
    """Сериалайзер создания пользователей."""

    first_name = serializers.CharField(
        label=_('Имя'),
        required=True,
        allow_blank=False,
        max_length=50,  # noqa: WPS432
    )
    last_name = serializers.CharField(
        label=_('Фамилия'),
        required=True,
        allow_blank=False,
        max_length=50,  # noqa: WPS432
    )
    email = serializers.EmailField(
        label=_('Адрес электронной почты'),
        required=True,
    )
    phone = PhoneNumberField(
        label=_('Телефон'),
        required=False,
        allow_blank=True,
        max_length=12,  # noqa: WPS432
    )
    role = serializers.CharField(
        label=_('Роль'),
        required=True,
        allow_blank=False,
        max_length=20,  # noqa: WPS432
    )
    companies = serializers.ListField(
        label=_('Компания, за которыми необходимо закрепить пользователя'),
        required=True,
        allow_null=False,
        child=serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all(),
        ),
        write_only=True,
    )

    def validate_avatar(self, avatar):
        """Корректность файла для аватарки."""
        if avatar and avatar.extension not in settings.ALLOWED_AVATARS:  # type: ignore  # noqa: E501
            raise ValidationError([_('Некорректный тип файла.')])
        return avatar

    def validate_role(self, role: str) -> str:
        """Проверка корректности введенной роли."""
        if role not in CompanyUserRole.values:
            raise ValidationError([_('Некорректная роль пользователя.')])
        return role

    def create(self, validated_data):  # noqa: WPS210
        """Новый пользователь является не активным.

        Пользователь, которого добавили через api является не активным.
        Изменение активности происходит после установки пароля.
        """
        phone = validated_data.get('phone', '')
        companies = validated_data.get('companies')
        role = validated_data.get('role')
        request = self.context.get('request')
        # Удаляем из username информацию о почтовом ящике.
        username = validated_data.get('email').split('@')[0]
        # Создаем пользователя.
        self.instance = User.objects.create(
            username=username,
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            is_active=False,
        )
        # Создаем профиль пользователя и набор стандартных графиков.
        Profile.objects.create(
            user=self.instance,
            phone=phone,
        )
        # Связываем пользователя и компаниями.
        CompanyUsers.objects.bulk_create(
            [
                CompanyUsers(
                    company=company,
                    user=self.instance,
                    role=role,
                    creator_id=request.user.pk,
                )
                for company in companies
            ],
        )
        for company in companies:
            # Отправляем нужные уведомления.
            url = absolute_backend_endpoint(
                app_name='cicada',
                action_name='companies-detail',
                request=request,
                object_id=company.pk,
            )
            notify_user_about_consolidation_company.apply_async(
                kwargs={
                    'company_pk': company.pk,
                    'user_pk': self.instance.pk,
                    'url': url,
                },
            )

        return self.instance
