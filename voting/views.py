from django.shortcuts import render
from .models import Voting, Element

# Create your views here.


def home(request):
    context = {
        'votings': Voting.objects.all(),
        'elements': Element.objects.all(),
    }
    return render(request, 'voting/home.html', context)

