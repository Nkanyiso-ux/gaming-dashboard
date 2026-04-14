from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view,name='dashboard'),
<<<<<<< HEAD
    path('overview', views.overview,name='overview'),#default page
=======
    path('overview/', views.overview,name='overview'),#default page
>>>>>>> 7ca17e07060172a71a63ea8aaffc785142cf3297
    path('delete/<int:id>/', views.delete_session,name='delete_session'),
   # path('export/', views.views.eport_excel,name='export_excel'),
    
]
