from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path('merge/', views.Merge.as_view(), name='merge'),
    path('merge/setup/', views.MergeSetup.as_view(), name='mergesetup'),  # расположение файлов отностительно друг друга
    # path('merge/ready/', views.MergeReady.as_view(), name='mergeready'),

    path('split/', views.Split.as_view(), name='split'),
    path('split/setup/', views.SplitSetup.as_view(), name='splitsetup'),  # сохранить в zip или дать несколько ссылок
    # path('split/next/', views.SplitReady.as_view(), name='splitready'),

    path('rotate/', views.Rotate.as_view(), name='rotate'),
    path('rotate/setup/', views.RotateSetup.as_view(), name='rotatesetup'),  # угол поворота для всех страниц
    # path('rotate/ready/', views.RotateReady.as_view(), name='rotateready'),

    path('delete/', views.Delete.as_view(), name='delete'),
    path('delete/setup/', views.DeleteSetup.as_view(), name='deletesetup'),  # номера страниц для удаления
    # path('delete/ready/', views.DeleteReady.as_view(), name='deleteready'),
    
    path('convert_to_zip/', views.Convert.as_view(), name='convert'),
    path('convert_to_zip/setup/', views.Convert.as_view(), name='convertsetup'),  # имя zip файла, степень сжатия
    path('convert_to_zip/ready/', views.ConvertReady.as_view(), name='convertready'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
