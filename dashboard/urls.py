from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view,name='login'),
    path("register/", views.register_view, name="register"),
    path('overview', views.overview,name='overview'),
    path('sessions/', views.dashboard_view,name='dashboard'),#defalt page
    path('delete/<int:id>/', views.delete_session,name='delete_session'),
    path('edit/<int:id>/', views.edit_session, name='edit_session'),
    path('logout/', views.logout_view,name='logout'),
    path('export/', views.export_excel, name='export_excel'),
]
