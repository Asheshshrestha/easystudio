from django.urls import path
from apps.v1.services import views

urlpatterns = [
    # path("",views.ListPackageAPIView.as_view(),name = "servicetype_list"),
    path("service-type/create/",views.CreateServiceTypeAPIView.as_view()),
    path("service-type/<int:pk>/detail/",views.ServiceTypeDetailAPIView.as_view()),
    path("service-type/<int:pk>/update/",views.UpdateServiceTypeAPIView.as_view()),
    path("service-type/<int:pk>/activeinactive/",views.ActiveInactiveServiceTypeAPIView.as_view()),
    path("service-type/<int:pk>/delete/",views.DestroyServiceTypeAPIView.as_view()),
    path("service-type/<int:pk>/list/",views.StudioServiceTypeListAPIView.as_view()),

    path("<int:pk>/accept/",views.ReceivedServiceRequestAPIView.as_view()),
    path("<int:pk>/printed/",views.PrintedServiceRequestAPIView.as_view()),
    path("<int:pk>/cancel/",views.CancelServiceRequestAPIView.as_view()),
    path("<int:pk>/delete/",views.DestroyRequestServiceAPIView.as_view()),
    path("create/",views.RequestServiceAPIView.as_view()),
    path("requestlist/studio/",views.MyServiceRequestStudioAPIView.as_view()),
    path("requestlist/user/",views.MyServiceRequestUserAPIView.as_view()),
    path("<int:pk>/detail/",views.RequestServiceDetailAPIView.as_view()),
    path("<int:pk>/update/",views.UpdateRequestServiceAPIView.as_view()),

]