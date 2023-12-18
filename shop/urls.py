from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('paintings/', views.painting_list, name='paintings'),
    path('paintings/<slug:category_slug>/', views.painting_list, name='paintings_by_category'),
    path('paintings/<int:id>/<slug:slug>/', views.painting_detail, name='paintings_detail'),
]