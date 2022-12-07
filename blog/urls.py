from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add_post/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update_post/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete_post/', PostDeleteView.as_view(), name='post_delete'),
]
