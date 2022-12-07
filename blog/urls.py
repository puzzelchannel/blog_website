from django.urls import path

from .views import post_list, post_detail, create_post

urlpatterns = [
    path('', post_list, name='posts_list'),
    path('<int:id>/', post_detail, name='posts_detail'),
    path('add_post/', create_post, name='post_create'),
]
