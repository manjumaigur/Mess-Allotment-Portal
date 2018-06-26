from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from mess.models import Mess
# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	profile_pic = models.FileField(null=True, help_text="upload jpg, jpeg, png files only", validators=[FileExtensionValidator(['jpg','png','jpeg'])])
	roll_no = models.CharField(max_length=7, null=True)
	admission_no = models.IntegerField(null=True)
	mess_no = models.IntegerField(null=True)
	mobile_no = models.IntegerField(null=True)
	GENDER_CHOICES = (
		('M','Male'),
		('F','Female'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
	is_mess_alloted = models.BooleanField(default=False)
	alloted_mess = models.ForeignKey(Mess, on_delete=models.CASCADE, unique=False, null=True)
  
	def get_absolute_url(self):
		return reverse('accounts:dashboard', kwargs={'pk': self.pk})

	def __str__(self):
		return self.user.username

class HostelOfficial(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	employee_id = models.CharField(max_length=10, null=True)
	mobile_no = models.IntegerField(null=True)
	designation = models.CharField(max_length=100, null=True)

	def get_absolute_url(self):
		return reverse('accounts:dashboard', kwargs={'pk':self.pk})

	def __str__(self):
		return self.user.username

class Manager(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	manager_id = models.CharField(max_length=10, null=True)
	mobile_no = models.IntegerField(null=True)

	def get_absolute_url(self):
		return reverse('accounts:dashboard', kwargs={'pk':self.pk})

	def __str__(self):
		return self.user.username


