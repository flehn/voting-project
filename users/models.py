from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    total_number_of_votings = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'


    # Wir überschreiben hier die Save Method, damit die Profilbilder mit einer max Größe von 300x300 gespeichert werden.
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)






