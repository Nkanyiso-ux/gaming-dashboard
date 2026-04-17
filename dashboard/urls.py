from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview,name='overview'),
    path('sessions/', views.dashboard_view,name='dashboard'),#defalt page
    path('delete/<int:id>/', views.delete_session,name='delete_session')   
]
