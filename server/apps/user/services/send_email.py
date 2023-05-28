from allauth.account.utils import user_pk_to_url_str, user_username
from django.contrib.sites.shortcuts import get_current_site
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from allauth import account

from server.apps.services.exception import SendEmailError
from allauth.account.forms import default_token_generator
from allauth.utils import build_absolute_uri
from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse

from server.apps.user.models import User


def send_confirm_email(  # noqa: WPS210, C901
    user: User,
    request: Request,
) -> None:
    """Отправка письма со ссылкой для подтверждения регистрации."""
    temp_key = default_token_generator.make_token(user)
    path = reverse(
        settings.USERS_CONFIRM_EMAIL_REVERSE_URL,  # type: ignore
        kwargs={'extra_path': f'{user.email}/{temp_key}'},
    )
    url = build_absolute_uri(request, path)
    url_without_api = url.replace('api/user/users/', '')

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
