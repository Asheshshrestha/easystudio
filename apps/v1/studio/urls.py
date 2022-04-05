from django.urls import path
from apps.v1.studio import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from apps.v1.package.views import MyStudioPackageAPIView
urlpatterns = [
    path("list/",views.ListStudioAPIView.as_view()),
    path("create/",views.StudioRegistrationView.as_view()),
    path("profile/",views.StudioProfileView.as_view()),
    path("update/",views.UpdateStudioProfile.as_view()),
     path('package/',include('apps.v1.package.urls')),
     path('service/',include('apps.v1.services.urls')),
     path("mypackages/",MyStudioPackageAPIView.as_view()),
     path("rate/",views.RateStudio.as_view()),
     path("<int:pk>/getrate/",views.GetStudioRating.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
