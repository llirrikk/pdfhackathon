from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('merge/', views.Merge.as_view(), name='merge'),
    path('merge/next/', views.MergeNext.as_view(), name='mergenext'),
    path('split/', views.Split.as_view(), name='split'),
    path('rotate/', views.Rotate.as_view(), name='rotate'),
    path('delete/', views.Delete.as_view(), name='delete'),
    path('convert_to_zip/', views.Convert.as_view(), name='convert'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
