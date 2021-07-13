from django.urls import path
from . import views
from .views import (
    VotingListView,
    VotingListViewUserRestricted,
    VotingDetailView,
    VotingCreateView,
    VotingUpdateView,
    VotingDeleteView,
)



urlpatterns = [
    #path('', views.home, name='voting-home'),
    path('', VotingListView.as_view(), name='list-of-votings'),
    path('my-votings/', VotingListViewUserRestricted.as_view(), name='list-of-votings-userrestricted'),
    path('<int:pk>/', VotingDetailView.as_view(), name='voting-detail'),
    path('new/', VotingCreateView.as_view(), name='voting-create'),
    path('<int:pk>/update/', VotingUpdateView.as_view(), name='voting-update'),
    path('<int:pk>/delete/', VotingDeleteView.as_view(), name='voting-delete'),
]