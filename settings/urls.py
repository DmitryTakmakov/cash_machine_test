from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from itemsapp.views import CreateReceiptView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cash_machine/', CreateReceiptView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
