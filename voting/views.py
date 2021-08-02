from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Count
from .models import Voting, Element
from .forms import CreateElementForm
from random import sample
from django.contrib import messages
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
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = Voting.objects.filter(active=True, private=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['votingelements'] = Voting.objects.filter(private=False, active=True).annotate(num__element=Count('related_votings'))
        return context





class VotingListViewUserRestricted(LoginRequiredMixin, ListView):
    model = Voting
    template_name = 'voting/list-of-votings-userrestricted.html'
    context_object_name = 'voting'
    ordering = ['date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_votings'] = Voting.objects.filter(author=self.request.user, active=True).annotate(num__element=Count('related_votings'))
        context['deactive_votings'] = Voting.objects.filter(author=self.request.user, active=False).annotate(num__element=Count('related_votings'))
        #context['anzahlelemente'] = Voting.objects.filter(author=self.request.user).annotate('related_votings')
        return context

    def get_queryset(self):
        queryset = Voting.objects.filter(author=self.request.user)
        return queryset


    """""
    In Case that the corresponding Elements of the different votings should be displayed as well
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        votings = Voting.objects.filter(author=self.request.user)
        for element in votings:
            # related_votings is a related_name parameter in the ForeignKey definition of the ElementModel
            context[element.id] = element.related_votings.all()
        return context
    """



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
        context['ordered_elements'] = Element.objects.filter(voting_id=self.kwargs['pk']).order_by('-likes')[:3]
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
def activate(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    element = Element.objects.filter(voting_id=pk)
    if len(element) > 1:
        voting.active ^= True
        voting.save()
    else:
        messages.warning(request, f'You cannot activate a Voting with less than two Items. Please add Items.')
    return redirect('list-of-votings-userrestricted')


def private(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    voting.private ^= True
    voting.save()
    return redirect('voting-detail', pk)

""""
def vote_view(request, pk):
    vote = get_object_or_404(Voting_Element, pk=pk)
    name = Voting_Element.objects.get(pk=pk)
    vote.number_votes += 1
    vote.save()
    messages.success(request, f'Voted for {name.title}')
    return redirect('voting_page')
"""


# ELEMENT
class ActiveVoting(DetailView):
    template_name = "voting/active-voting.html"

    def get_queryset(self):
        queryset = Voting.objects.filter(id=self.kwargs['pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        # This updates the number of votes, each time the page is requested
        Voting.objects.filter(id=self.kwargs['pk']).update(number_of_votes=F('number_of_votes') + 1)

        return super().get(request, *args, **kwargs)

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


def vote_view(request, pk, pk_element):
    element = get_object_or_404(Element, pk=pk_element)
    element.likes += 1
    element.save()
    messages.success(request, f'Voted for {element.title}')
    return redirect('voting-active', pk)
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

class RankElementsListview(ListView):
    model = Element
    template_name = 'voting/voting-results.html'
    ordering = ['-likes']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the corresponding elements
        context['elements'] = Element.objects.filter(voting_id=self.kwargs['pk']).order_by('-likes')
        # Add in a the current Voting in order to display Voting Name
        context['voting'] = Voting.objects.filter(id=self.kwargs['pk'])
        return context
