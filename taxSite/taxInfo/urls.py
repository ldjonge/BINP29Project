from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('getId',views.getId, name='getId'),
    path('<int:idNumber>/', views.results, name='results'),
    path('invalid',views.invalid, name='invalid'),
]
