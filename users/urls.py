from django.urls import path
from .views import SetPhotoView, registerPage, loginPage, logoutPage, ProfileView, UpdateProfileView, \
                            PasswordsChangeView, UserPostsView, MakePostView,EditPostView, \
                            SetPhotoView    
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('edit-post/<slug:slug>/', EditPostView.as_view(),name="edit_post"),
    path('create-post/', MakePostView.as_view(),name="create_post"),
    path('my-posts/', UserPostsView.as_view(), name="my_posts"),
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/reset_password_confirm_done.html'), 
    name="password_reset_complete"),
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="reset_password/reset_password_confirm.html"), 
    name='password_reset_confirm'),
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name='reset_password/reset_password_done.html'),
    name="password_reset_done"),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html'), name='reset_password'),
    path('password/', PasswordsChangeView.as_view(template_name='change_password.html'), name='ch_password'),
    path('set-photo/', SetPhotoView.as_view(), name='set_photo'),
    path('update-info/', UpdateProfileView.as_view(), name='update_info'),
    path('my-profile/', ProfileView.as_view(), name='my_profile'),
    path('reg/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
]