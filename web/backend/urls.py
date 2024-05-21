from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", csrf_exempt(views.download.as_view()), name='download'),
]
