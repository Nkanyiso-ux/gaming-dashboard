from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view,name='dashboard'),
    path('overview/', views.overview,name='overview'),#default page
    path('delete/<int:id>/', views.delete_session,name='delete_session'),
   # path('export/', views.views.eport_excel,name='export_excel'),
    
]
