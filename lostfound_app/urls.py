from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('add/found/', views.add_found_item, name='add_found_item'),
    path('add/lost/', views.add_lost_item, name='add_lost_item'),

    path('found/edit/<int:item_id>/', views.edit_found_item, name='edit_found_item'),
    path('found/delete/<int:item_id>/', views.delete_found_item, name='delete_found_item'),

    path('lost/edit/<int:item_id>/', views.edit_lost_item, name='edit_lost_item'),
    path('lost/delete/<int:item_id>/', views.delete_lost_item, name='delete_lost_item'),

    path('item/<str:item_type>/<int:item_id>/', views.item_detail, name='item_detail'),
]
