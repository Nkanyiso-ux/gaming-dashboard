from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview,name='overview'),#default page
    path('sessions/', views.dashboard_view,name='dashboard'),
    path('delete/<int:id>/', views.delete_session,name='delete_session'),
   # path('export/', views.views.eport_excel,name='export_excel'),
    
]
