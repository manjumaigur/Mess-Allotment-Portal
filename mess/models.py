from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.

class Mess(models.Model):
	name = models.CharField(max_length=50)
	caterer_name = models.CharField(max_length=200)
	manager_name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	address = models.CharField(max_length=100)
	is_veg = models.BooleanField(default=True)
	is_nonVeg = models.BooleanField(default=False)
	GENDER_CHOICES = (
		('M','Male'),
		('F','Female'),
	)
	gender_intake = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
	intake = models.IntegerField(null=True)
	is_full = models.BooleanField(default=False)
	present_strength = models.IntegerField(default=0)

	def get_absolute_url(self):
		return reverse('mess:mess_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.name

class Fee(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	transaction_no = models.CharField(max_length=20,null=True)
	fees = models.FloatField(null=True)
	paid_on = models.DateTimeField(null=True)
	fees_receipt = models.FileField(null=True,help_text="upload pdf file less than 2mb",)
	is_fees_paid = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('mess:fee_detail', kwargs={'pk': self.pk})

	def __str__(self):
		return self.transaction_no