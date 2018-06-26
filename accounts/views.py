from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, HostelOfficial, Manager
from mess.models import Fee
from .forms import UserForm, StudentForm, HostelOfficialForm, ManagerForm, UserEditForm
# Create your views here.

def home_page(request):
	if request.user.is_authenticated:
		return redirect('mess:index')
	return render(request, 'accounts/home_page.html',{})

def login_view(request):
	if request.method == 'POST':
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('mess:index')
	    else:
	    	messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request,'accounts/login.html', {'form' : form})

@login_required
def logout_view(request):
	logout(request)
	return render(request, 'accounts/logged_out.html',{})

@login_required
def dashboard(request):
	try:
		if request.user.student:
			profile = get_object_or_404(Student,pk=request.user.student.id)
	except:
		pass
	try:
		if request.user.hostelofficial:
			profile = get_object_or_404(HostelOfficial,pk=request.user.hostelofficial.id)
	except:
		pass
	try:
		if request.user.manager:
			profile = get_object_or_404(Manager,pk=request.user.manager.id)
	except:
		pass
	return render(request,'accounts/dashboard.html',{'profile':profile})


def register(request,profile_role):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password2'])
			new_user.save()
			if profile_role == 'student':
				new_profile = Student.objects.create(user=new_user)
				new_fees = Fee.objects.create(user=new_user)
				new_profile.save()
				new_fees.save()
				return redirect('accounts:student-register', pk=new_profile.id)
			elif profile_role == 'official':
				new_profile = HostelOfficial.objects.create(user=new_user)
				new_profile.save()
				return redirect('accounts:official-register', pk=new_profile.id)
			elif profile_role == 'manager':
				new_profile = Manager.objects.create(user=new_user)
				new_profile.save()
				return redirect('accounts:manager-register', pk=new_profile.id)
			else:
				return redirect('accounts:register')
	else:
		user_form = UserForm()	
	return render(request, 'accounts/register.html',{'form':user_form,'role':profile_role})

def student_register(request,pk):
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		form = StudentForm(request.POST, request.FILES, instance=student)
		if form.is_valid():
			form.save()
			return redirect('accounts:login')
	else:
		form = StudentForm(instance=student)
	return render(request, 'accounts/student_register.html',{'form':form})

def official_register(request,pk):
	official = get_object_or_404(HostelOfficial, pk=pk)
	if request.method == 'POST':
		form = HostelOfficialForm(request.POST, instance=official)
		if form.is_valid():
			form.save()
			return redirect('accounts:dashboard')
	else:
		form = HostelOfficialForm(instance=official)
	return render(request, 'accounts/official_register.html',{'form':form})

def manager_register(request,pk):
	manager = get_object_or_404(Manager, pk=pk)
	if request.method == 'POST':
		form = ManagerForm(request.POST, instance=manager)
		if form.is_valid():
			form.save()
			return redirect('accounts:dashboard')
	else:
		form = ManagerForm(instance=manager)
	return render(request, 'accounts/manager_register.html',{'form':form})

@login_required
def edit_student(request):
	if not request.user.student:
		return redirect('accounts:logout')
	student = get_object_or_404(Student, pk=request.user.student.id)
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, instance=request.user)
		student_form = StudentForm(request.POST, request.FILES, instance=student)
		if user_form.is_valid() and student_form.is_valid():
			user_form.save()
			student_form.save()
			return redirect('accounts:dashboard')
	else:
		user_form = UserEditForm(instance=request.user)
		student_form = StudentForm(instance=student)
	return render(request, 'accounts/profile_edit.html',{'user_form':user_form, 'profile_form':student_form})

@login_required
def edit_manager(request):
	if not request.user.manager:
		return redirect('accounts:logout')
	manager = get_object_or_404(Manager, pk=request.user.manager.id)
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, instance=request.user)
		manager_form = ManagerForm(request.POST, instance=manager)
		if user_form.is_valid() and manager_form.is_valid():
			user_form.save()
			manager_form.save()
			return redirect('accounts:dashboard')
	else:
		user_form = UserEditForm(instance=request.user)
		manager_form = ManagerForm(instance=manager)
	return render(request, 'accounts/profile_edit.html',{'user_form':user_form, 'profile_form':manager_form})

@login_required
def edit_official(request):
	if not request.user.hostelofficial:
		return redirect('accounts:logout')
	official = get_object_or_404(HostelOfficial, pk=request.user.hostelofficial.id)
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, instance=request.user)
		official_form = HostelOfficialForm(request.POST, instance=official)
		if user_form.is_valid() and official_form.is_valid():
			user_form.save()
			official_form.save()
			return redirect('accounts:dashboard')
	else:
		user_form = UserEditForm(instance=request.user)
		official_form = HostelOfficialForm(instance=official)
	return render(request, 'accounts/profile_edit.html',{'user_form':user_form, 'profile_form':official_form})

@login_required
def student_details(request,pk):
	try:
		try:
			if request.user.hostelofficial:
				student = get_object_or_404(Student, pk=pk)
		except:
			pass

		try:	
			if request.user.manager:
				student = get_object_or_404(Student, pk=pk)
		except Manager.DoesNotExist:
			redirect('mess:index')
		return render(request, 'accounts/student_details.html' , {'profile':student})

	except HostelOfficial.DoesNotExist:
		messages.error(request, "You're not allowed to perform this action")
		redirect('mess:index')

@login_required
def student_list(request):
	try:
		if request.user.hostelofficial:
			students = Student.objects.all()
			return render(request, 'accounts/student_list.html', {'students' : students})
	except HostelOfficial.DoesNotExist:
		messages.error(request, "You're not allowed to perform this action")
		redirect('mess:index')	
