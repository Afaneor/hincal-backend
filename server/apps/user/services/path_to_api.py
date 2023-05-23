from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.conf import settings
from rest_framework.reverse import reverse


def path_for_front(user, request) -> str:
    """Изменение конечного url для установки пароля.

    Для front необходимо чтобы ссылка не содержала данные api, то есть
    конечный url из вида /api/user/users/reset-password/.../ преобразуется
    в /set-password/.../.
    """
    path = reverse(
        settings.USERS_PASSWORD_RESET_REVERSE_URL,  # type: ignore
        kwargs={
            'extra_path':
                f'{user_pk_to_url_str(user)}-' +  # noqa: WPS237
                str(default_token_generator.make_token(user)),
        },
    )
    absolute_path = build_absolute_uri(request, path)
    return absolute_path.replace('api/user/users/re', '')
