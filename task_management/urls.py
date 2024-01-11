
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/account/', include('accounts.urls')),
    path('api/v1/task-board/', include('task_board.urls')),
    path('api/v1/notification/', include('notification.urls')),
    path('api/v1/message/', include('chat.urls')),
]
urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)