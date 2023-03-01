from django.urls import path
from .views import *

urlpatterns = [

    path('create-company/', CompanyView.as_view(), name='create-company'),
    path('list-company/', CompanyView.as_view(), name='all-companys'),
    path('company/<int:pk>/', CompanyListByIdView.as_view(), name='company-detail'),
    path('delete-company/<int:pk>', CompanyView.as_view(), name='delete-company'),
    path('update-company/<int:pk>', CompanyView.as_view(), name='update-company'),

]
