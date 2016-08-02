from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from jobslist.views import (
	index,
	employer,
	job,
	employer_register,
	applicant_register,
	add_job,
	user_login,
	user_logout,
	employer_edit,
	job_edit,
	jobslist,
	employers,
	my_password_change,
	my_password_change_done,
	signup,
	)
	
urlpatterns = [
	url(r'^$', index, name='index-view'),
	url(r'^edit/employer/(?P<employer_name_slug>[\w\-]+)/$', employer_edit, name='employer_edit-view'),
	url(r'^edit/job/(?P<employer_name_slug>[\w\-]+)/(?P<job_title_slug>[\w\-]+)/$', job_edit, name='job_edit-view'),
	url(r'^signup/$', signup, name='signup-view'),
	url(r'^register/employer/$', employer_register, name='employer_register-view'),
	url(r'^register/applicant/$', applicant_register, name='applicant_register-view'),
	url(r'^addjob/(?P<employer_name_slug>[\w\-]+)/$', add_job, name='add_job-view'),
	url(r'^login/$', user_login, name='login-view'),
	url(r'^logout/$', user_logout, name='logout-view'),
	url(r'^jobs/$', jobslist, name='jobslist-view'),
	url(r'^employers/$', employers, name='employers-view'),
	url('^password_change/$', my_password_change, name='password_change-view'),
	url('^password_change/done/$', my_password_change_done, name='password_change_done'),
	url(r'^(?P<employer_name_slug>[\w\-]+)/$', employer, name='employer-view'),
	url(r'^(?P<employer_name_slug>[\w\-]+)/(?P<job_title_slug>[\w\-]+)/$', job, name='job-view'),
	]
	
