from server.settings.components import config

MAX_STRING_LENGTH = 255

# Переменные для работы DaData.
DADATA_API_TOKEN = config('DADATA_API_TOKEN', default='token', cast=str)
DADATA_API_URL = config(
    'DADATA_API_URL',
    default='https://suggestions.dadata.ru/suggestions/api/4_1/rs',
    cast=str,
)
DADATA_TIMEOUT_SEC = 5
