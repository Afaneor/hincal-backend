"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView
from health_check import urls as health_urls

admin.autodiscover()

urlpatterns = [
    # Health checks:
    path('health/', include(health_urls)),  # noqa: DJ05
    path('api-auth/', include('rest_framework.urls')),
    re_path(
        '^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$',
        CustomPasswordResetFromKeyView.as_view(),
        name='account_reset_password_from_key',
    ),
    # include main:
    path('', include(main_urls, namespace='main')),

    *admin_urlpatterns,
    *docs_urlpatterns,
    *jwt_urlpatterns,
    *seo_urlpatterns,
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = (
        [
            # URLs specific only to django-debug-toolbar:
            path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
        ] + urlpatterns +
        static(
            # Serving media files in development only:
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    )
