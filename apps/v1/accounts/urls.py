from django.urls import path
from apps.v1.accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("users/create/",views.UserRegistrationView.as_view()),
    path("users/login/",views.UserLoginView.as_view()),
    path("users/profile/",views.UserProfileView.as_view()),
    path("studio/profile/",views.StudioProfileView.as_view()),
    path("users/updatemyprofile/",views.UpdateMyProfile.as_view()),
    path("users/<int:pk>/update/",views.UpdateUserView.as_view()),
    path("users/changepassword/",views.ChangePasswordView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
