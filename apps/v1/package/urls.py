from django.urls import path
from apps.v1.package import views


urlpatterns = [
    path("",views.ListPackageAPIView.as_view(),name = "list_news"),
    path("create/",views.CreatePackageAPIView.as_view()),
    path("<int:pk>/",views.PackageDetailAPIView.as_view()),
    path("<int:pk>/update/",views.UpdatePackageAPIView.as_view()),
    path("<int:pk>/activeinactive/",views.ActiveInactivePackageAPIView.as_view()),
    path("<int:pk>/delete/",views.DestroyPackageAPIView.as_view()),
    path("<int:pk>/packages/",views.StudioPackageListAPIView.as_view()),
]