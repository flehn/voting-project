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

)



urlpatterns = [
    #path('', views.home, name='voting-home'),
    path('', VotingListView.as_view(), name='list-of-votings'),
    path('my-votings/', VotingListViewUserRestricted.as_view(), name='list-of-votings-userrestricted'),
    path('<int:pk>/', VotingDetailView.as_view(), name='voting-detail'),
    path('new/', VotingCreateView.as_view(), name='voting-create'),
    path('<int:pk>/update/', VotingUpdateView.as_view(), name='voting-update'),
    path('<int:pk>/delete/', VotingDeleteView.as_view(), name='voting-delete'),

    path('<int:pk>/active/', ActiveVoting.as_view(), name='voting-active'),

    path('<int:pk>/add-elements/', views.createelement, name='add-elements'),
    path('<int:pk>/<int:pk_element>/', ElementDetailview.as_view(), name="element-detail"),
    path('<int:pk>/<int:pk_element>/update/', ElementUpdateView.as_view(), name='element-update'),
    path('<int:pk>/<int:pk_element>/delete/', ElementeDeleteview.as_view(), name="delete-element"),

]