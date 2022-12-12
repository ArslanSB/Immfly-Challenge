from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'contents', views.ContentViewSet)
router.register(r'channels', views.ChannelViewSet)
router.register(r'channels/(?P<id>[0-9]+)', views.ChannelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]