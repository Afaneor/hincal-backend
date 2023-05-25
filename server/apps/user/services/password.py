import re

from allauth import account
from allauth.account.forms import default_token_generator
from allauth.account.utils import url_str_to_user_pk, user_username, \
    user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.timezone import now
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.reverse import reverse

from server.apps.services.exception import ApiError
from server.apps.user.models import User

# Регулярное выражение для проверки на корректность пути сброса пароля
RESET_PASSWORD_REGEXP = re.compile('(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)')


def get_user_reset_password_process(extra_path: str) -> AbstractUser:
    """Проверка валидности токена сброса пароля."""
    # Выделяем необходимые нам параметры для сброса пароля
    match = RESET_PASSWORD_REGEXP.match(extra_path)
    if match:
        uidb36, key = match.groups()

        return get_user_by_token(uidb36, key)

    raise ApiError(
        _('Не удалось извлечь id пользователя и ключ сброса пароля'),
    )


def get_user_by_token(uidb36_inner: str, key: str) -> AbstractUser:
    """Получение пользователя по ключу и id пользователя."""
    pk = url_str_to_user_pk(uidb36_inner)

    try:
        reset_user = User.objects.get(pk=pk)
    except (ValueError, User.DoesNotExist):
        raise ApiError(_('Пользователь не найден'))

    invalid_token = not default_token_generator.check_token(
        reset_user,
        key,
    )
    if reset_user is None or invalid_token:
        raise ApiError(_('Токен сброса пароля не действителен'))
    return reset_user


def send_email_with_reset_password(
    user: User,
    request: Request,
) -> None:
    """Отправка пользователю письма со сбросом пароля."""
    path = reverse(
        settings.USERS_PASSWORD_RESET_REVERSE_URL,  # type: ignore
        kwargs={
            'extra_path':
                f'{user_pk_to_url_str(user)}-' +  # noqa: WPS237
                str(default_token_generator.make_token(user)),
        },
    )
    url = build_absolute_uri(request, path)
    url_without_api = url.replace('api/user/users', '')

    context = {
        'current_site': get_current_site(request),
        'user': user,
        'password_reset_url': url_without_api,
        'request': request,
        'year': now().year,
    }

    method = account.app_settings.AUTHENTICATION_METHOD
    if method != account.app_settings.AuthenticationMethod.EMAIL:
        context['username'] = user_username(user)  # noqa: WPS226
    account.adapter.get_adapter(request).send_mail(
        'account/email/password_reset_key', user.email, context,
    )


def set_new_password(extra_path: str, password: str):
    """Установка нового пароля для пользователя."""
    user = get_user_reset_password_process(extra_path=extra_path)
    user.set_password(password)

    # Активация аккаунта пользователя и создание профиля.
    if not user.is_active:
        user.is_active = True

    user.save(update_fields=['password', 'is_active'])


def check_new_password(password1: str, password2: str) -> None:
    """Проверка совпадения и корректности нового пароля."""
    if password1 != password2:
        raise ValidationError(
            {
                'new_password': [
                    _(
                        'Пароли должны совпадать! ' +
                        'Проверьте корректность данных',
                    ),
                ],
            },
        )
    try:
        validate_password(str(password1))
    except DjangoValidationError as exc:
        raise ValidationError(exc)
