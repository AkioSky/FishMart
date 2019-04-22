from django.db import models
from saleor.account.models import PossiblePhoneNumberField
from saleor.account.models import User


# Create your models here.
class RequestOrder(models.Model):
    slug = models.SlugField(unique=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    phone = PossiblePhoneNumberField(blank=True, default='')
    fish_name = models.CharField(max_length=200)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.slug
