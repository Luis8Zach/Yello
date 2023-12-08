from django.urls import path
from .views import (
    home,
    register,
    editar,
    delete,
    profile,
    follow,
    unfollow,
    like_post,
    post_detail,
    add_comment,
    top_creators
)
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='twitter/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:post_id>/', delete, name='delete'),
    path('profile/<str:username>/', profile, name='profile'),
    path('editar/', editar, name='editar'),
    path('follow/<str:username>/', follow, name='follow'),
    path('unfollow/<str:username>/', unfollow, name='unfollow'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('like/<int:pk>/', like_post, name='like_post'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('top_creators/', top_creators, name='top_creators'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
