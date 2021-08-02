from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Voting(models.Model):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    # one-many | one User can have multiple Votings
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('voting-detail', kwargs={'pk': self.pk})


class Element(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='related_votings')
    likes = models.PositiveIntegerField(default=0)
    link = models.CharField(max_length=300, blank=True, default='https://images.pexels.com/photos/2444429/pexels-photo-2444429.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')

    def __str__(self):
        return self.title


# create an voting object 'Voting01' and than add the link the elements with  voting01.voting = element01
