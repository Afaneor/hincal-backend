from django.contrib import admin

from server.apps.blog.models import Post, Support


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    """Класс админки постов."""

    list_display = (
        'id',
        'title',
        'is_published',
    )
    search_fields = (
        'title',
        'tags',
    )
    list_filter = (
        'is_published',
    )
    ordering = (
        'id',
        'title',
        'is_published',
    )


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin[Support]):
    """Класс админки для мер поддержек."""

    list_display = (
        'id',
        'title',
        'is_actual',
    )
    search_fields = (
        'title',
        'tags',
    )
    list_filter = (
        'is_actual',
    )
    ordering = (
        'id',
        'title',
        'is_actual',
    )
