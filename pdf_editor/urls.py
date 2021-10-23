from django.urls import include, path
from . import views

urlpatterns = [
    path(r'/', views.main, name='main'),
    path('merge/', views.Merge.as_view(), name='merge'),
    path('split/', views.Split.as_view(), name='split'),
    path('rotate/', views.Rotate.as_view(), name='rotate'),
    path('delete/', views.Delete.as_view(), name='delete'),
    path('convert_to_zip/', views.Convert.as_view(), name='convert'),
]
