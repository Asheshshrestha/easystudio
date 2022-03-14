from django.urls import path
from apps.v1.accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("users/create/",views.CreateUserView.as_view()),
    path("users/<int:pk>/update/",views.UpdateUserView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
