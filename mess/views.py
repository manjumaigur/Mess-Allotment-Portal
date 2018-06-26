from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Mess, Fee
from accounts.models import Student, HostelOfficial, Manager
from .forms import MessForm, MessEditForm, FeeForm
# Create your views here.

@method_decorator(login_required, name='dispatch')
class MessIndex(generic.ListView):
	context_object_name = 'mess_list'
	template_name = 'mess/index.html'

	def get_queryset(self):
		return Mess.objects.all()

@login_required
def mess_detail(request, pk):
	mess = get_object_or_404(Mess, pk = pk)
	return render(request, 'mess/mess_detail.html', {'mess' : mess})

@login_required
def mess_create(request):
	try:
		if request.user.hostelofficial:
			if request.method == 'POST':
				form = MessForm(data=request.POST)
				if form.is_valid():
					mess = form.save()	
					if mess.present_strength == mess.intake:
						mess.is_full = True
						mess.save()
					messages.success(request, "Mess created")
					return redirect('mess:mess_detail', pk=mess.id)
			else:
				form = MessForm()
			return render(request, 'mess/mess_create.html', {'form' : form})
	except HostelOfficial.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def mess_edit(request,pk):
	try:
		if request.user.hostelofficial:
			mess = get_object_or_404(Mess, pk=pk)
			if request.method == 'POST':
				form = MessEditForm(request.POST, instance=mess)
				if form.is_valid():
					mess = form.save()	
					if mess.present_strength == mess.intake:
						mess.is_full = True
						mess.save()
					messages.success(request, "Mess details updated")
					return redirect('mess:mess_detail',pk=mess.id)
			else:
				form = MessEditForm(instance=mess)
			return render(request, 'mess/mess_edit.html', {'form' : form})
	except HostelOfficial.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def mess_members(request,pk):
	try:
		try:
			if request.user.hostelofficial:
				mess = get_object_or_404(Mess,pk=pk)
				mess_members = mess.student_set.all()
		except:
			pass

		try:
			if request.user.manager:
				mess = get_object_or_404(Mess,pk=pk)
				if mess.manager_name == request.user:
					mess_members = mess.student_set.all()
				else:
					messages.error(request, "You're not manager of that particular mess")
					return redirect('mess:index')
		except:
			pass

		return render(request, 'mess/mess_members.html', {'mess_members' : mess_members})
		
	except:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def mess_choose(request):
	try:
		student = request.user.student
		if student:
			if student.is_mess_alloted:
				messages.info(request, "Mess already alloted")
				return redirect('mess:mess_allot', pk=student.alloted_mess.id)
			mess_list = Mess.objects.filter(gender_intake=student.gender)
			return render(request, 'mess/mess_choose.html',{'mess_list':mess_list})
	except Student.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def mess_allot(request,pk):
	try:
		member = request.user.student
		if member:
			if not request.user.fee.is_fees_paid:
				messages.error(request, "First pay the fees")
				return redirect('mess:pay_fees')
			if not request.user.fee.verified:
				messages.error(request, "Fees details not verified, please contact officials")
				return redirect('mess:fee_details', pk=request.user.fee.id)
			mess = get_object_or_404(Mess, pk=pk)
			if member.is_mess_alloted:
				messages.info(request, "Mess already alloted")
				return render(request, 'mess/mess_alloted.html', {})
			if mess.is_full:
				messages.error(request, "Selected mess is full, please select another one")
				return redirect('mess:mess_choose')
			if mess.gender_intake == member.gender:
				member.is_mess_alloted = True
				member.alloted_mess = mess
				mess.present_strength += 1
				if mess.present_strength == mess.intake:
					mess.is_full = True
				mess.save()
				member.save() 
				return render(request, 'mess/mess_alloted.html', {})
			else:
				messages.error(request, "Selected is mess is for different gender, Please select another one")
				return redirect('mess:mess_choose')
	except Student.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def mess_card(request):
	try:
		profile = request.user.student
		if profile:
			if profile.is_mess_alloted:
				return render(request, 'mess/mess_card.html', {'profile':profile})
			else:
				messages.info(request, "Mess not alloted, please select choose a mess")
				return redirect('mess:mess_choose')
	except Student.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')


@login_required
def pay_fees(request):
	try:
		if request.user.student:
			fees = get_object_or_404(Fee, pk=request.user.fee.id)
			if request.method == 'POST':
				fees_form = FeeForm(request.POST, request.FILES, instance=fees)
				if fees_form.is_valid():
					fees = fees_form.save(commit=False)
					fees.user = request.user
					fees.is_fees_paid = True
					fees.transaction_no = fees_form.cleaned_data['transaction_no']
					fees.fees = fees_form.cleaned_data['fees']
					fees.paid_on = fees_form.cleaned_data['paid_on']
					fees.fees_receipt = fees_form.cleaned_data['fees_receipt']
					fees.save()
					messages.success(request, "Fee payment details updated")
					return redirect('mess:fee_details', pk=fees.id)
			else:
				fees_form = FeeForm(instance=fees)
			return render(request, 'mess/pay_fees.html', {'form':fees_form})
	except Student.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def edit_fees(request,pk):
	try:
		if request.user.student:
			fees = get_object_or_404(Fee, pk=pk)
			if request.method == 'POST':
				fees_form = FeeForm(request.POST, request.FILES, instance=fees)
				if fees_form.is_valid():
					fees = fees_form.save(commit=False)
					fees.user = request.user
					fees.is_fees_paid = True
					fees.save()
					messages.success(request, "Fee payment details updated")
					return redirect('mess:fee_details', pk=fees.id)
			else:
				fees_form = FeeForm(instance=fees)
			return render(request, 'mess/pay_fees.html', {'form':fees_form})
	except Student.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:index')

@login_required
def fee_details(request,pk):
	fees = get_object_or_404(Fee, pk=pk)
	return render(request, 'mess/fee_details.html', {'fees':fees})

@login_required
def fee_verify(request,pk):
	try:
		if request.user.hostelofficial:
			fees = get_object_or_404(Fee, pk=pk)
			if fees.is_fees_paid:
				fees.verified = True
				fees.save()
				messages.success(request, "Fees details verified")
				return redirect('mess:fee_details', pk=fees.pk)
			else:
				messages.info(request, "Fees not paid")
				return redirect('mess:fee_details', pk=pk)
	except:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:fee_details', pk=pk)

@login_required
def fee_reject(request,pk):
	try:
		if request.user.hostelofficial:
			fees = get_object_or_404(Fee, pk=pk)
			fees.verified = False
			fees.is_fees_paid = False
			fees.save()
			if fees.user.student.is_mess_alloted:
				fees.user.student.is_mess_alloted = False
				fees.user.student.alloted_mess.clear()
				#mess.present_strength -= 1

			return redirect('mess:fee_details', pk=pk)
	except HostelOfficial.DoesNotExist:
		messages.error(request, "You're not permitted to perform this action")
		return redirect('mess:fee_details', pk=pk)

