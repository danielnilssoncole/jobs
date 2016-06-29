from django.contrib import admin
from jobslist.models import Employer, Job, Applicant

class EmployerAdmin(admin.ModelAdmin):
	list_display = ('company_Name', 'field', 'location', 'website')

class JobAdmin(admin.ModelAdmin):
	list_display = ('title', 'employer', 'location', 'salary', 'updated_datetime', 'pub_datetime')

class ApplicantAdmin(admin.ModelAdmin):
	list_display = ('user', 'first_name', 'last_name', 'location')


admin.site.register(Employer, EmployerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Applicant, ApplicantAdmin)


