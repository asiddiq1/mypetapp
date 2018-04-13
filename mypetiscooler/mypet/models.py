from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Mypets(models.Model):
    petowner = models.ForeignKey(User)
    petname = models.CharField(max_length=100)
    species = models.CharField(max_length=200)
    #photo = models.FileField(upload_to='photo/', default="")
    def __str__(self):
        return 'petname='+ self.petname + ', species='+ self.species



class MypetsImage(models.Model):
    mypets = models.ForeignKey(Mypets)
    image = models.ImageField(upload_to='photo/')

class PetBattleImages(models.Model):
    image1 = models.CharField(max_length=100)
    image1_count = models.IntegerField(default=0, blank=True)
    image2 = models.CharField(max_length=100)
    image2_count = models.IntegerField(default=0, blank=True)

