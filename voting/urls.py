from django.urls import path
from . import views
from .views import (
    VotingListView,
    VotingListViewUserRestricted,
    VotingDetailView,
    VotingCreateView,
    VotingUpdateView,
    VotingDeleteView,
    ElementeDeleteview,
    ElementDetailview,
    ElementUpdateView,
    ActiveVoting,
    RankElementsListview,
)



urlpatterns = [
    #path('', views.home, name='voting-home'),

    path('', VotingListView.as_view(), name='list-of-votings'),
    path('home/', VotingListView.as_view(), name='voting-home'),
    path('my-votings/', VotingListViewUserRestricted.as_view(), name='list-of-votings-userrestricted'),
    path('<int:pk>/', VotingDetailView.as_view(), name='voting-detail'),
    path('new/', VotingCreateView.as_view(), name='voting-create'),
    path('<int:pk>/update/', VotingUpdateView.as_view(), name='voting-update'),
    path('<int:pk>/delete/', VotingDeleteView.as_view(), name='voting-delete'),

    path('<int:pk>/acxx', views.activate, name='activate'),
    path('<int:pk>/prixx', views.private, name='private'),
    path('<int:pk>/active/', ActiveVoting.as_view(), name='voting-active'),

    path('<int:pk>/results/', RankElementsListview.as_view(), name='voting-results'),

    path('<int:pk>/add-elements/', views.createelement, name='add-elements'),
    path('<int:pk>/<int:pk_element>/', ElementDetailview.as_view(), name="element-detail"),
    path('<int:pk>/<int:pk_element>/update/', ElementUpdateView.as_view(), name='element-update'),
    path('<int:pk>/<int:pk_element>/delete/', ElementeDeleteview.as_view(), name="delete-element"),
    path('<int:pk>/<int:pk_element>/like', views.vote_view, name='like-element'),

]