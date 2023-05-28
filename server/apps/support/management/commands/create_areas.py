import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from server.apps.hincal.models import TerritorialLocation
from server.apps.support.models import Area


class Command(BaseCommand):
    """Добавление данных в Area."""

    help = 'Добавление данных в Area'

    def handle(self, *args, **options):  # noqa: WPS110
        """Добавление данных в Area."""

        url = 'https://investmoscow.ru/business/site-list?PerPage=1000'
        base_url = 'https://investmoscow.ru'
        areas = []

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        technopark_items = soup.find_all('a', class_='technopark__item')

        # Формируем объекты Area.
        for technopark_item in technopark_items:
            territorial_location = TerritorialLocation.objects.get(
                shot_name__iexact=technopark_item.find('div', class_='fs-14 mb-1').find('b').next_sibling.replace('\r\n', '').strip(),
            )
            areas.append(
                Area(
                    preview_image=f"{base_url}{technopark_item.find('img').attrs.get('data-src').strip()}",
                    title=technopark_item.find('h3').contents[0].replace('\\', '').strip(),
                    text=technopark_item.find('div', class_='fs-14 mt-1').find('b').next_sibling.replace('\r\n', '').replace('&NoBreak;', '').strip(),
                    territorial_location=territorial_location,
                    address=technopark_item.find('div', class_='fs-14 mt-1 mb-1').find('b').next_sibling.replace('\r\n', '').strip(),
                    site=f"{base_url}{technopark_item.attrs.get('href').strip()}",
                )
            )

        Area.objects.bulk_create(areas)
