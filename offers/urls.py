from django.urls import path

from . import views

app_name = "offers"

urlpatterns = [
    path("", views.offer_map, name="map"),
    path("new/", views.offer_create, name="create"),
    path("<int:pk>/", views.offer_detail, name="detail"),
    path("<int:pk>/share/", views.share_offer, name="share"),
]
