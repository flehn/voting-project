from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Voting, Element
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# Create your views here.


def home(request):
    context = {
        'votings': Voting.objects.all(),
        'elements': Element.objects.all(),
        'voting-of-this-user': Voting.objects.filter(username='name').first(),
    }
    return render(request, 'voting/list-of-votings.html', context)

# Class-based Views gucken immer nach einem Template mit der Naming-Convention:
# <app-name> / <model-name>_<viewtype.html>
# also hier voting/Voting_list.html
class VotingListView(ListView):
    model = Voting
    template_name = 'voting/list-of-votings.html'
    context_object_name = 'voting'
    ordering = ['date_created']

    def get_queryset(self):
        queryset = Voting.objects.filter(active=True)
        return queryset


class VotingListViewUserRestricted(LoginRequiredMixin, ListView):
    model = Voting
    template_name = 'voting/list-of-votings.html'
    context_object_name = 'voting'
    ordering = ['date_created']

    def get_queryset(self):
        queryset = Voting.objects.filter(author=self.request.user)
        return queryset

class VotingDetailView(LoginRequiredMixin, DetailView):
    model = Voting

class VotingCreateView(LoginRequiredMixin, CreateView):
    model = Voting
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UserPassesTestMixin checks if the user is the owner
class VotingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Voting
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        #self.get_object() gets the current voting object
        voting = self.get_object()
        #self.request.user gives the current logged in user
        if self.request.user == voting.author:
            return True
        return False

class VotingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Voting
    success_url = reverse_lazy('list-of-votings-userrestricted')

    def test_func(self):
        #self.get_object() gets the current voting object
        voting = self.get_object()
        #self.request.user gives the current logged in user
        if self.request.user == voting.author:
            return True
        return False