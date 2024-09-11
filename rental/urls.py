from django.urls import path, include
from rest_framework import routers

from rental import views

router = routers.DefaultRouter()
router.register(prefix="rooms", viewset=views.RoomViewSet, basename="rooms")
router.register(prefix="beds", viewset=views.BedViewSet, basename="beds")
router.register(prefix="posts", viewset=views.PostViewSet, basename="posts")
router.register(prefix="rental-contacts", viewset=views.RentalContactViewSet, basename="rental-contacts")

urlpatterns = [path("", include(router.urls))]
