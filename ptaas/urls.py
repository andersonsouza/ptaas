import os

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

for app in settings.INSTALLED_APPS:
    if not app.startswith('django.'):
        if os.path.exists(os.path.join(settings.BASE_DIR, '%s/urls.py' % (app))):
            urlpatterns += [
                url(r'^%s/' % (app), include('%s.urls' % (app))),
            ]
