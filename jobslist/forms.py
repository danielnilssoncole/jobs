from django import forms
from django.contrib.auth.models import User
from jobslist.models import Employer, Job, Applicant

class UserForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class EmployerForm(forms.ModelForm):
	size = forms.IntegerField(required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	location = forms.CharField(max_length=128, label='Headquarters Location')
	contact = forms.EmailField(max_length=128, label='Contact Email for Applicants')
	
	class Meta:
		model = Employer
		fields = ('company_Name', 'field', 'size', 'location', 'website', 'contact')
		
	def clean(self):
		cleaned_data = self.cleaned_data
		website = cleaned_data.get('website')
		
		if website and not website.startswith(('http://', 'https://')):
			website = 'http://' + website
			cleaned_data['website'] = website
		
		return cleaned_data
		
class JobForm(forms.ModelForm):
	#slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	
	class Meta:
		model = Job
		exclude = ('employer', 'slug')
		
class ApplicantForm(forms.ModelForm):
	location = forms.CharField(required=False)
	
	class Meta:
		model = Applicant
		fields = ('first_name', 'last_name', 'location')
	