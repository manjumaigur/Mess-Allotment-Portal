from django import forms
from .models import Mess, Fee
from accounts.models import Manager

class MessForm(forms.ModelForm):
	manager_name = forms.ModelChoiceField(queryset = Manager.objects.all(), required = True),
	class Meta:
		model = Mess
		fields = ['name','caterer_name','manager_name','address','is_veg','is_nonVeg','intake','gender_intake',]
		widgets = {'gender':forms.RadioSelect()}

class MessEditForm(forms.ModelForm):
	class Meta:
		model = Mess
		fields = ['name','caterer_name','manager_name','address','is_veg','is_nonVeg','intake','gender_intake',]
		widgets = {'gender':forms.RadioSelect()}

class FeeForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = ['transaction_no', 'fees', 'paid_on', 'fees_receipt',]