from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newfile.pdf',views.pdfPreview,name ='preview'),
]