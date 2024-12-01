from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('hr/admin/home/', views.admin_home, name='admin_home'),
    path('hr/user/home/', views.user_home, name='user_home'),
    path('hr/logout/', views.logout_view, name='logout'),
    path('hr/admin/users/', views.users_list, name='users_list'),
    path('hr/admin/add-user/', views.add_user, name='add_user'),
    path('hr/admin/edit-user/<uuid:user_id>/', views.edit_user, name='edit_user'),
    path('hr/admin/delete-user/<uuid:user_id>/', views.delete_user, name='delete_user'),
]
