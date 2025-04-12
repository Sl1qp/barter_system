from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [

    path("ads/", views.AdListView.as_view(), name="ad-list"),
    path("ads/create/", views.AdCreateView.as_view(), name="ad-create"),
    path("ads/<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("ads/<int:pk>/edit/", views.AdUpdateView.as_view(), name="ad-edit"),
    path("ads/<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad-delete"),

    path("proposals/", views.ProposalListView.as_view(), name="proposal-list"),
    path("proposals/create/", views.ProposalCreateView.as_view(), name="proposal-create"),
    path("proposals/<int:pk>/update/", views.ProposalUpdateView.as_view(), name="proposal-update"),
    path("proposals/<int:pk>/delete/", views.ProposalDeleteView.as_view(), name="proposal-delete"),

]
