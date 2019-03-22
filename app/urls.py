
from django.urls import path,include
from app import view_live,view_dir

urlpatterns = [
    path('live/' , include(view_live)),
    path('dir/' , include(view_dir)),
]
