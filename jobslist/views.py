from django.shortcuts import render, get_object_or_404, redirect
from jobslist.models import Employer, Job, Applicant
from jobslist.forms import UserForm, EmployerForm, JobForm, ApplicantForm
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.contrib.auth.models import User


def index(request):
	jobslist = Job.objects.order_by('-updated_datetime')[:5]
	employerslist = Employer.objects.order_by('-size')[:5]
	context= {
		'jobs': jobslist,
		'employers': employerslist,
		}
	
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	
	reset_last_visit_time = False
	
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		
		if (datetime.now() - last_visit_time).seconds > 0:
			visits += 1
			reset_last_visit_time = True
	
	else:
		reset_last_visit_time = True
	
	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	
	context['visits'] = visits
	response = render(request, 'jobslist/index.html', context)
	
	return response 
	
	
def employer(request, employer_name_slug):
	context = {}
	
	employer = get_object_or_404(Employer, slug = employer_name_slug)
	context['employer_name'] = employer.company_Name
		
	jobs = Job.objects.filter(employer=employer)
	jobs = jobs.order_by('-updated_datetime')
	context['jobs'] = jobs
	context['employer'] = employer
	context['employer_name_slug'] = employer_name_slug
	context['field'] = employer.field
	context['size'] = employer.size
	context['location'] = employer.location
	context['website'] = employer.website
	context['picture'] = employer.picture
	
	if employer.user == request.user:
		context['match'] = True
	
	return render(request, 'jobslist/employer.html', context)

@login_required	
def job(request, employer_name_slug, job_title_slug):
	context = {}
		
	employer = get_object_or_404(Employer, slug = employer_name_slug)
	job = get_object_or_404(employer.job_set, slug = job_title_slug)
		
	context['employer_name'] = employer.company_Name
	context['employer'] = employer
	context['employer_name_slug'] = employer_name_slug
	context['field'] = employer.field
	context['size'] = employer.size
	context['headquarters'] = employer.location
	context['email'] = employer.contact
	context['website'] = employer.website
		
	context['job'] = job
	context['title'] = job.title
	context['location'] = job.location
	context['salary'] = job.salary
	context['description'] = job.description 
	context['updated'] = job.updated_date
	context['job_title_slug'] = job_title_slug
	
	if employer.user == request.user:
		context['match'] = True
	
	return render(request, 'jobslist/job.html', context)
	

# def employer_register(request):
# 	
# 	registered = False
# 	
# 	if request.method == 'POST':
# 		user_form = UserForm(data=request.POST)
# 		employer_form = EmployerForm(data=request.POST)
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		
# 		if user_form.is_valid() and employer_form.is_valid():
# 			user = user_form.save()
# 			user.set_password(user.password)
# 			user.save()
# 			
# 			employer = employer_form.save(commit=False)
# 			employer.user = user
# 			
# 			if 'picture' in request.FILES['picture']:
# 				employer.picture = request.FILES['picture']
# 			
# 			employer.save()
# 			registered = True
# 			u = authenticate(username=username, password=password)
# 			
# 			if u is not None:
# 				if u.is_active:
# 					login(request, u)
# 			
# 		
# 		else:
# 			print user_form.errors, employer_form.errors
# 	
# 	else:
# 		user_form = UserForm()
# 		employer_form = EmployerForm()
# 		
# 	context = {}
# 	context['user_form'] = user_form
# 	context['employer_form'] = employer_form
# 	context['registered'] = registered
# 		
# 	return render(request, 'jobslist/employer_register.html', context)


def employer_register(request):
	
	context = {}
	registered = False
	
	if request.method == 'POST':
		#employer_form = EmployerForm(data=request.POST)
		employer_form = EmployerForm(request.POST, request.FILES)
		
		if employer_form.is_valid():
			employer = employer_form.save(commit=False)
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
			
			u = authenticate(username=username, password=password)
			if u is None:
				user = User.objects.create_user(username, email, password) 
				user.set_password(password)
				user.save()
	
				employer.user = user
				
				if 'picture' in request.FILES.keys():
					if 'picture' in request.FILES['picture']:
						employer.picture = request.FILES['picture']
			
				employer.save()
				registered = True
				us = authenticate(username=username, password=password)
			
				if us is not None:
					if us.is_active:
						login(request, us)
			
			else:
				error = 'That username is already taken :('
				context['error'] = error
		
		else:
			print employer_form.errors
	
	else:
		employer_form = EmployerForm()
		
	context['employer_form'] = employer_form
	context['registered'] = registered

	return render(request, 'jobslist/employer_register.html', context)

@login_required		
def add_job(request, employer_name_slug):
	emp = get_object_or_404(Employer, slug = employer_name_slug)
	
	if not request.user == emp.user:
		return HttpResponseRedirect('/jobslist/')
		
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			if emp:
				job = form.save(commit=False)
				job.employer = emp
				job.views = 0
				job.save()
				
				for jo in emp.job_set.all():
					count = 0
					if job.slug in jo.slug:
						count += 1
					else:
						count = count
				job.slug += str(count)
				job.save()
				
				return employer(request, employer_name_slug)
		else:
			print form.errors
	else:
		form = JobForm()
		
	context = {
		'form': form,
		'employer': emp,
		'employer_name_slug': employer_name_slug,
		'employer_name': emp.company_Name}
		
	return render(request, 'jobslist/add_job.html', context)
	
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/jobslist/')
			else:
				error = 'Your account is disabled.'
				return render(request, 'jobslist/login.html', {'error': error})
		else:
			error = 'Incorrect username or password.'
			return render(request, 'jobslist/login.html', {'error': error})
	
	else:
		return render(request, 'jobslist/login.html', {})
		
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/jobslist/')

@login_required	
def employer_edit(request, employer_name_slug):
	emp = get_object_or_404(Employer, slug = employer_name_slug)
	
	if not request.user == emp.user:
		return HttpResponseRedirect('/jobslist/')
		
	updated = False
	
	form = EmployerForm(request.POST or None, instance=emp)
	if form.is_valid():
		#form.save()
		empl = form.save(commit=False)
		
		if 'picture' in request.FILES:
			empl.picture = request.FILES['picture']
			
		empl.save()
		updated = True
		return employer(request, employer_name_slug)
	else:
		print form.errors
	
	context = {'form': form,
				'emp': emp,
				'updated': updated,}
	return render(request, 'jobslist/employer_edit.html', context)
	
@login_required	
def job_edit(request, employer_name_slug, job_title_slug):
	emp = get_object_or_404(Employer, slug = employer_name_slug)
	jobs = Job.objects.filter(employer = emp)
	j = get_object_or_404(emp.job_set, slug = job_title_slug) 
				
	if not request.user == emp.user:
		return HttpResponseRedirect('/jobslist/')
		
	updated = False
	
	form = JobForm(request.POST or None, instance=j)
	if form.is_valid():
		form.save()
		updated = True
		return job(request, employer_name_slug, job_title_slug)
	else:
		print form.errors
	
	context = {'form': form,
				'emp': emp,
				'job': j,
				'job_title_slug': j.slug,
				'updated': updated,}
	return render(request, 'jobslist/job_edit.html', context)
	
# def applicant_register(request):
# 	
# 	registered = False
# 	
# 	if request.method == 'POST':
# 		user_form = UserForm(data=request.POST)
# 		applicant_form = ApplicantForm(data=request.POST)
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		
# 		if user_form.is_valid() and applicant_form.is_valid():
# 			user = user_form.save()
# 			user.set_password(user.password)
# 			user.save()
# 			
# 			applicant = applicant_form.save(commit=False)
# 			applicant.user = user
# 			applicant.save()
# 			registered = True
# 			u = authenticate(username=username, password=password)
# 			
# 			if u is not None:
# 				if u.is_active:
# 					login(request, u)
# 		
# 		else:
# 			print user_form.errors, applicant_form.errors
# 	
# 	else:
# 		user_form = UserForm()
# 		applicant_form = ApplicantForm()
# 		
# 	context = {}
# 	context['user_form'] = user_form
# 	context['applicant_form'] = applicant_form
# 	context['registered'] = registered
# 		
# 	return render(request, 'jobslist/applicant_register.html', context)
	

def applicant_register(request):
	
	context = {}
	registered = False
	
	if request.method == 'POST':
		applicant_form = ApplicantForm(data=request.POST)
		
		if applicant_form.is_valid():
			applicant = applicant_form.save(commit=False)
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password']
			
			u = authenticate(username=username, password=password)
			if u is None:
				user = User.objects.create_user(username, email, password) 
				user.set_password(password)
				user.save()
			
				applicant.user = user
				applicant.save()
				registered = True
				us = authenticate(username=username, password=password)
			
				if us is not None:
					if us.is_active:
						login(request, us)
						
			else:
				error = 'That username is already taken :('
				context['error'] = error
		
		else:
			print applicant_form.errors
	
	else:
		applicant_form = ApplicantForm()
		
	context['applicant_form'] = applicant_form
	context['registered'] = registered
		
	return render(request, 'jobslist/applicant_register.html', context)
	
def jobslist(request):
	jobs = Job.objects.order_by('-updated_datetime')
	context = {'jobs': jobs}
	return render(request, 'jobslist/jobslist.html', context)
	
def employers(request):
	employers = Employer.objects.order_by('company_Name')
	context = {'employers': employers}
	return render(request, 'jobslist/employers.html', context)
	
def my_password_change(request):
	template_response = auth_views.password_change(request, template_name='jobslist/passwordchange.html')
	return template_response
	
def my_password_change_done(request):
	template_response = auth_views.password_change_done(request, template_name='jobslist/passwordchangedone.html')
	return template_response
	
def signup(request):
	context = {}
	return render(request, 'jobslist/signup.html', context)
    
	
	
	

		
		


