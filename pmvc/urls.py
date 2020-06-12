from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'videos', views.VideoViewSet)

app_name = 'pmvc'

urlpatterns = [
    path('', views.index, name='index'),
    path('account_home', views.AccountHome, name='AccountHome'),
    path('account_selection_handler', views.AccountSelectionHandler, name='AccountSelectionHandler'),
    path('account_selected/<int:account_id>', views.AccountSelected, name='AccountSelected'),
    path('account_create', views.AccountCreate, name='AccountCreate'),
    path('list_videos/<int:account_id>', views.ListVideos, name='ListVideos'),
    path('ingest_video/<int:account_id>', views.IngestVideo, name='IngestVideo'),
    path('tester', views.tester, name='Tester'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)