import django_filters
from django.contrib.auth import get_user_model, login, logout
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.services.views import RetrieveListCreateViewSet
from server.apps.user.api.serializers import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    LoginSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
    UserSerializer,
)
from server.apps.user.services.serializers.password import (
    get_user_reset_password_process,
    send_email_with_reset_password,
    set_new_password,
)

User = get_user_model()


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


class UserViewSet(RetrieveListCreateViewSet):
    """Пользователь. Просмотр/создание.

    Описание: Админы платформы могут добавить пользователя в систему, а сами
    пользователи могут только просматривать информацию.
    Изменение информации о пользователе (ФИО) доступно через профиль.
    Добавление/регистрация пользователя происходит через POST запрос.

    Доступно: суперпользователю и владельцу уведомлений.
    """

    serializer_class = UserSerializer
    create_serializer_class = CreateUserSerializer
    queryset = User.objects.select_related('profile')
    filterset_class = UserFilter
    ordering_fields = '__all__'
    permission_type_map = {
        **RetrieveListCreateViewSet.permission_type_map,
        'logout': 'action_is_authenticated',
        'login': None,
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
