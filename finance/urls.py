
from django.urls import path, include
from rest_framework import routers
from moviments import views

router = routers.DefaultRouter()
router.register("moviments", views.MovimentView)

urlpatterns = [
	path("", include(router.urls))	
]
