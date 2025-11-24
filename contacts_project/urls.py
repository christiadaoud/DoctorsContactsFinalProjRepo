from django.contrib import admin
from django.urls import path
from contactlist import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctor_list'),

    path('doctors/add/', views.doctor_add, name='doctor_add'),
    path('doctors/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),

    path('recommend/', views.recommend_doctors, name='recommend_doctors'),
]

