from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('change-password/', views.ChangePasswordView.as_view(), name="change-password"),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="users-detail"),
    path('posts/', views.PostList.as_view(), name="posts"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="posts-detail"),
    path('comments/', views.CommentList.as_view(), name="comments"),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name="comments-detail"),
]