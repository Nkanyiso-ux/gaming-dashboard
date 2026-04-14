from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view,name='dashboard'),#defalt page
    path('overview/', views.overview,name='overview'),
    path('delete/<int:id>/', views.delete_session,name='delete_session')   
]
