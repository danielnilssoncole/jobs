from django import forms
from django.contrib.auth.models import User
from jobslist.models import Employer, Job, Applicant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions

class UserForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
# class EmployerForm(forms.ModelForm):
# 	size = forms.IntegerField(required=False)
# 	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
# 	location = forms.CharField(max_length=128, label='Headquarters Location')
# 	contact = forms.EmailField(max_length=128, label='Contact Email for Applicants')
# 	
# 	class Meta:
# 		model = Employer
# 		fields = ('company_Name', 'field', 'size', 'location', 'website', 'contact', 'picture')
# 		
# 	def clean(self):
# 		cleaned_data = self.cleaned_data
# 		website = cleaned_data.get('website')
# 		
# 		if website and not website.startswith(('http://', 'https://')):
# 			website = 'http://' + website
# 			cleaned_data['website'] = website
# 		
# 		return cleaned_data
		

class EmployerForm(forms.ModelForm):
	size = forms.IntegerField(required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	location = forms.CharField(max_length=128, label='Headquarters Location')
	contact = forms.EmailField(max_length=128, label='Contact Email for Applicants')
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	username = forms.CharField(label="Username", required=True, max_length=128, min_length=4)
	
	class Meta:
		model = Employer
		fields = ('company_Name', 'field', 'size', 'location', 'website', 'contact', 'picture')
		
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.layout = Layout(
		Field('username', css_class='input-sm', placeholder='Username'),
		Field('email', css_class='input-sm', placeholder='Email'),
		Field('password', css_class='input-sm', placeholder='Password'),
		Field('company_Name', css_class='input-sm', placeholder='Company Name'),
		Field('field', css_class='input-sm', placeholder='Field'),
		Field('size', css_class='input-sm', placeholder='Size'),
		Field('location', css_class='input-sm', placeholder='City, ST'),
		Field('website', css_class='input-sm', placeholder='Website'),
		Field('contact', css_class='input-sm', placeholder='contact@example.com'),
		Field('picture'),
		FormActions(Submit('submit', 'Submit', css_class='btn-primary'))
		)
		
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
	email = forms.EmailField(widget=forms.EmailInput())
	password = forms.CharField(widget=forms.PasswordInput())
	username = forms.CharField(label="Username", required=True, max_length=128, min_length=4)
	
	class Meta:
		model = Applicant
		fields = ('first_name', 'last_name', 'location')
		
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.layout = Layout(
		Field('username', css_class='input-sm', placeholder='Username'),
		Field('email', css_class='input-sm', placeholder='Email'),
		Field('password', css_class='input-sm', placeholder='Password'),
		Field('first_name', css_class='input-sm', placeholder='First Name'),
		Field('last_name', css_class='input-sm', placeholder='Last Name'),
		Field('location', css_class='input-sm', placeholder='City, ST'),
		FormActions(Submit('submit', 'Submit', css_class='btn-primary'))
		)
	