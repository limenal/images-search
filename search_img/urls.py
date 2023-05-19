from django.urls import path
from . import views

urlpatterns = [
    path("", views.SearchImageView.as_view())
]
