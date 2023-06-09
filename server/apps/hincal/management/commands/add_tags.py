import random
from typing import List

from django.core.management.base import BaseCommand
from django.db.models import Max

from server.apps.blog.models import Post
from server.apps.hincal.models import Sector, Equipment
from server.apps.support.models import Area, Offer, Support


def random_sector(count: int) -> List[str]:
    max_id = Sector.objects.all().aggregate(max_id=Max('id'))['max_id']
    sector_tags = []

    while len(sector_tags) != count:
        pk = random.randint(1, max_id)
        sector = Sector.objects.filter(pk=pk).first()
        if sector:
            sector_tags.append(sector.slug)

    return sector_tags


class Command(BaseCommand):
    """Добавление тегов."""

    help = 'Добавление тегов.'

    def handle(self, *args, **options):  # noqa: WPS110
        """Добавление тегов к сущностям."""
        for area in Area.objects.all():
            area.tags.add(
                area.territorial_location.slug,
                *random_sector(2),
            )
        print('Добавлены теги для Area')

        for offer in Offer.objects.all():
            offer.tags.add(*random_sector(3))
        print('Добавлены теги для Offer')

        for support in Support.objects.all():
            support.tags.add(*random_sector(3))
        print('Добавлены теги для Support')

        for post in Post.objects.all():
            post.tags.add(*random_sector(3))
        print('Добавлены теги для Post')

        for equipment in Equipment.objects.all():
            equipment.tags.add(*random_sector(3))
        print('Добавлены теги для Equipment')
