from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('home',views.home, name='home'),
    path('report/<cloud>/<report>',views.report),
    path('export/<cloud>/<report>',views.exportPandas,name='exportToExcel')
]
