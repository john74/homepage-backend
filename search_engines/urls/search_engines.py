from django.urls import path

from search_engines import views


app_name = "search_engines"

urlpatterns = [
    path("", views.SearchEngineListAPIView.as_view(), name="list"),
    path("bulk-create/", views.SearchEngineBulkCreateAPIView.as_view(), name="bulk_create"),
    path("bulk-update/", views.SearchEngineBulkUpdateAPIView.as_view(), name="bulk_update"),
    path("bulk-delete/", views.SearchEngineBulkDeleteAPIView.as_view(), name="bulk_delete"),
]