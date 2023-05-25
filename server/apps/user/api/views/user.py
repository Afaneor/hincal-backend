import django_filters
from allauth.account.forms import default_token_generator
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from server.apps.services.views import RetrieveListCreateUpdateViewSet
from server.apps.user.api.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
    UserSerializer, RegisterSerializer, ConfirmEmailRequestSerializer,
    ConfirmEmailProcessSerializer,
)
from server.apps.user.models import User
from server.apps.user.services.create_user import create_new_user, \
    send_confirm_email
from server.apps.user.services.helper import get_django_user, check_extra_path, \
    get_user_by_email_and_check_token
from server.apps.user.services.password import (
    get_user_reset_password_process,
    send_email_with_reset_password,
    set_new_password,
)


class UserFilter(django_filters.FilterSet):
    """Фильтр для модели пользователя."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'is_active',
        )


class UserViewSet(RetrieveListCreateUpdateViewSet):
    """Пользователь. Просмотр/создание/изменение.

    Описание: Админы платформы могут добавить пользователя в систему, а сами
    пользователи могут только просматривать информацию.
    Изменение информации о пользователе (ФИО) доступно через профиль.
    Добавление/регистрация пользователя происходит через POST запрос.

    Доступно: суперпользователю и владельцу уведомлений.
    """

    serializer_class = UserSerializer
    queryset = User.objects.select_related('profile')
    filterset_class = UserFilter
    ordering_fields = '__all__'
    permission_type_map = {
        **RetrieveListCreateUpdateViewSet.permission_type_map,
        'login': None,
        'logout': 'action_is_authenticated',
        'reset_password_request': None,
        'reset_password_process': None,
        'change_password': 'action_is_authenticated',
    }

    def get_queryset(self):
        """Выдача информации о пользователях."""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(pk=user.pk)

    def create(self, request, *args, **kwargs):
        """Создание пользователя через api.

        После добавления пользователя отправляем на почту письмо с
        инструкцией по установке пароля.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Отправляем письмо с установкой пароля.
        send_email_with_reset_password(
            user=serializer.instance,
            request=request,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        ['POST'],
        url_path='login',
        detail=False,
        serializer_class=LoginSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def login(self, request):
        """Авторизация пользователя.

        Общее описание: пользователь с указанными данными авторизуется с
        помощью сессии.

        Доступно: любому пользователю.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # noqa: WPS204
        login(request, serializer.user)

        return Response(None, status=status.HTTP_200_OK)

    @action(
        ['POST'],
        detail=False,
        url_path='register',
        serializer_class=RegisterSerializer,
    )
    def register(self, request):  # noqa: WPS210
        """Регистрация пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_new_user(data=serializer.validated_data)

        user.set_password(serializer.validated_data.get('password1'))
        user.save()
        user.refresh_from_db()

        # Отправляем письмо активации пользователя
        send_confirm_email(
            request=request,
            user=user,
        )

        return Response(
            DetailedUserSerializer(user).data,  # type: ignore
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=['POST'],
        detail=False,
        url_path='resend-email-confirmation',
        serializer_class=ConfirmEmailRequestSerializer,
    )
    def confirm_email_request(self, request):
        """Повторная отправка сообщения об активации аккаунта.

        Общее описание: api позволяет направить письмо для активации аккаунта
        пользователя.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_django_user(serializer.validated_data.get('email'))
        send_confirm_email(
            user=user,
            request=request,
        )

        return Response(
            data={
                'detail': _(
                    'На указанный адрес электронной почты ' +
                    'отправлено письмо с подтверждением ' +
                    'регистрации',
                ),
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['GET', 'POST'],
        detail=False,
        url_path='confirm-email/(?P<extra_path>.+)?',
        serializer_class=ConfirmEmailProcessSerializer,
    )
    def confirm_email_process(self, request, extra_path=None):
        """Подтверждение регистрации."""
        if request.method == 'GET':
            email, key = check_extra_path(extra_path)
            return Response(
                data=UserSerializer(get_user_by_email_and_check_token(email, key)).data,
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email, key = check_extra_path(extra_path)
        user = get_user_by_email_and_check_token(email, key)

        if not default_token_generator.check_token(user, key):
            raise ValidationError(
                _('Некорректный ключ подтверждения активации'),
            )
        if user.is_active:
            return HttpResponseRedirect(settings.EMAIL_CONFIRM_REDIRECT_URL)
        user.is_active = True
        user.save()

        return HttpResponseRedirect(settings.EMAIL_CONFIRM_REDIRECT_URL)

    @action(
        methods=['GET'],
        detail=False,
        url_path='get-info',
        serializer_class=UserSerializer,
    )
    def get_info(self, request):
        """Получение информации о пользователе."""
        if request.user.is_authenticated:
            serializer = self.get_serializer(
                User.objects.get(id=request.user.id),
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(
        methods=['POST'],
        url_path='send-reset-password-email',
        detail=False,
        serializer_class=ResetPasswordRequestSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def reset_password_request(self, request):
        """Запрос сброса пароля.

        Общее описание: api позволяет запросить письмо с инструкцией по
        сбросу пароля.

        Доступно: любому пользователю.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_email_with_reset_password(
            user=serializer.user,
            request=request,
        )

        return Response(
            data={
                'detail':
                    _(
                        'На указанный адрес электронной почты отправлено ' +
                        'письмо с инструкцией по восстановлению пароля',
                    ),
            },
            status=status.HTTP_200_OK,
        )

    @action(  # type: ignore
        methods=['GET', 'POST'],
        detail=False,
        url_path='reset-password/(?P<extra_path>.+)?',
        serializer_class=ResetPasswordConfirmSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def reset_password_process(self, request, extra_path: str):
        """Сброс пароля пользователя.

        Общее описание: api позволяет установить новый пароль пользователю.

        Доступно: любому пользователю.
        """
        if request.method == 'GET':
            user = get_user_reset_password_process(extra_path)
            return Response(
                data=UserSerializer(user).data,  # type: ignore
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        set_new_password(
            extra_path=extra_path,
            password=serializer.validated_data.get('password1'),
        )

        return Response(
            data={'detail': _('Новый пароль успешно установлен')},
            status=status.HTTP_200_OK,
        )

    @action(
        ['PATCH', 'PUT'],
        detail=False,
        url_path='change-password',
        serializer_class=ChangePasswordSerializer,
    )
    def change_password(self, request):
        """Смена пароля.

        Общее описание: api позволяет изменить старый пароль на новый.

        Доступно: любому только авторизованному пользователю.
        """
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'detail': _('Пароль успешно изменен')},
            status=status.HTTP_200_OK,
        )

    @action(
        ['POST'],
        detail=False,
        url_path='logout',
    )
    def logout(self, request):
        """Выход из системы.

        Общее описание: api позволяет пользователю выйти из системы.

        Доступно: любому только авторизованному пользователю.
        """
        logout(request)

        return Response(
            data={'detail': _('Пользователь успешно вышел из системы')},
            status=status.HTTP_200_OK,
        )
