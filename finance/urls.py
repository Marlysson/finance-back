
from django.urls import path, include
from rest_framework import routers
from moviments import views

router = routers.SimpleRouter()
router.register("moviments", views.MovimentView)

urlpatterns = [
	path("", include(router.urls)),
	path("statistics", views.StatisticsView.as_view(), name="statistics")
]
