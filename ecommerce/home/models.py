from django.db import models
from django.urls import reverse
# Create your models here.
class categ(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)

    def __str__(self):
        return '{}' .format(self.name)

    def get_url(self):
        return reverse('categview',args=[self.slug])


class product(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)
    img=models.ImageField(upload_to='picture')
    descrip=models.TextField()
    stock=models.IntegerField()
    available=models.BooleanField()
    price=models.IntegerField()
    category=models.ForeignKey(categ,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}' .format(self.name)

    def get_url(self):
        return reverse('detail',args=[self.category.slug,self.slug])