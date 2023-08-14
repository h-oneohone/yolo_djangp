from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('traffic_sign', views.TrafficSignViewSet)

urlpatterns = router.urls
