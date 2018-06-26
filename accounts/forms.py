from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Manager, HostelOfficial

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2',]

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ['roll_no', 'admission_no', 'mess_no', 'gender', 'mobile_no', 'profile_pic',]
		widgets = {'gender':forms.RadioSelect()}

class ManagerForm(forms.ModelForm):
	class Meta:
		model = Manager
		fields = ['manager_id', 'mobile_no',]

class HostelOfficialForm(forms.ModelForm):
	class Meta:
		model = HostelOfficial
		fields = ['employee_id', 'mobile_no', 'designation',]


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email',]
		exclude = ['username','password1','password2',]