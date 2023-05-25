from django.contrib.sites.shortcuts import get_current_site
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from allauth import account

from server.apps.services.exception import SendEmailError
from server.apps.user.models import User
from server.apps.user.services.create_business import create_business
from allauth.account.forms import default_token_generator
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from rest_framework.request import Request
from rest_framework.reverse import reverse


def send_confirm_email(  # noqa: WPS210, C901
    user: AbstractUser,
    request: Request,
) -> None:
    """Отправка письма со ссылкой для подтверждения регистрации."""
    temp_key = default_token_generator.make_token(user)
    path = reverse(
        settings.USERS_CONFIRM_EMAIL_REVERSE_URL,  # type: ignore
        kwargs={'extra_path': f'{user.email}/{temp_key}'},
    )
    url = build_absolute_uri(request, path)
    url_without_api = url.replace('api/users/user/', '')

    context = {
        'current_site': get_current_site(request),
        'user': user,
        'activate_url': url_without_api,
        'request': request,
        'year': now().year,
    }
    try:
        account.adapter.get_adapter(request).send_mail(
            'account/email/email_confirmation', user.email, context,
        )
    except Exception:
        raise SendEmailError(
            detail=_(
                'Письмо с подтверждением регистрации не отправлено. ' +
                'Обратитесь в поддержку системы.',
            ),
        )


def create_new_user(data: dict) -> User:
    """Создание нового пользователя."""
    user = User.objects.create(
        username=data.get('email').split('@')[0],
        email=data.get('email'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        middle_name=data.get('middle_name'),
    )
    create_business(inn=data.get('inn'), user=user)
    return user
