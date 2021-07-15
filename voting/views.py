from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Voting, Element
from .forms import CreateElementForm
from random import sample
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
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


# ELEMENT & VOTING
class VotingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Voting

    def test_func(self):
        #self.get_object() gets the current voting object
        voting = self.get_object()
        #self.request.user gives the current logged in user
        if self.request.user == voting.author:
            return True
        return False

    # Darstellen aller Elemente die zu diesem einen Ranking gehören
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['elements'] = Element.objects.filter(voting_id=self.kwargs['pk'])
        return context


#Voting
class VotingCreateView(LoginRequiredMixin, CreateView):
    model = Voting
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#Voting
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

#Voting
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


# ELEMENT
class ElementDetailview(DetailView):
    model = Element

    def get_object(self):
        pk2 = self.kwargs['pk_element']
        element = get_object_or_404(Element, pk=pk2)
        return element


# ELEMENT DELETE
class ElementeDeleteview(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Element

    def get_object(self):
        pk2 = self.kwargs['pk_element']
        element = get_object_or_404(Element, pk=pk2)
        return element

    def test_func(self):
        #self.get_object() gets the current voting object
        element = self.get_object()
        #self.request.user gives the current logged in user
        if self.request.user == element.voting.author:
            return True
        return False


    def get_success_url(self):
        # voting = self.object.voting
        #Alternative: return reverse_lazy('voting-detail', kwargs={'voting.id': voting.id})
        return reverse_lazy('voting-detail', kwargs={'pk': self.kwargs['pk']})

# ELEMENT Update
class ElementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Element
    fields = ['title', 'description']

    # Dadurch das wir 2x IDs in der url haben: /<pk>/<pk.element> , müssen wir der Klasse mitteilen
    # dass pk_element das Objekt in der Datenbank ist, welches wir brauchen
    def get_object(self):
        pk2 = self.kwargs['pk_element']
        element = get_object_or_404(Element, pk=pk2)
        return element

    # Hier wird getestet, dass nur der Author bearbeiten kann.
    def test_func(self):
        #self.get_object() gets the current voting object
        element = self.get_object()
        #self.request.user gives the current logged in user
        if self.request.user == element.voting.author:
            return True
        return False

    # Wir leiten nach erfolgreicher Arbeit wieder zum zugehörigen Voting zurück, dafür müssen wir die Voting ID
    # mit parsen, ohne diese Funktion würde die elementen ID eingefügt.
    def get_success_url(self):
        # voting = self.object.voting
        #Alternative: return reverse_lazy('voting-detail', kwargs={'voting.id': voting.id})
        return reverse_lazy('voting-detail', kwargs={'pk': self.kwargs['pk']})


# ELEMENT CREATE
def createelement(request, pk):
    voting_instance = get_object_or_404(Voting, pk=pk)

    if request.method == 'POST':
        form = CreateElementForm(request.POST)

        if form.is_valid():
            element_instance = form.save(commit=False)
            element_instance.voting = voting_instance
            element_instance.save()
            return redirect('voting-detail', pk)
    else:
        form = CreateElementForm()

    context = {
        'form': form,
    }
    # pass this instance
    return render(request, 'voting/element_form.html', context)


# ACTIVE VOTING

# ELEMENT
class ActiveVoting(TemplateView):
    template_name = "voting/active-voting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['two_elements'] = self.get_random_element()
        return context

    def get_random_element(self):
        two_elements = []
        pks = Element.objects.filter(voting_id=self.kwargs['pk']).values_list('id', flat=True)
        random_pk = sample(list(pks), k=2)
        element1 = Element.objects.get(pk=random_pk[0])
        element2 = Element.objects.get(pk=random_pk[1])
        two_elements.append(element1)
        two_elements.append(element2)
        return two_elements


""""
    def get(self, request, *args, **kwargs):
        self.get_random_element()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

"""