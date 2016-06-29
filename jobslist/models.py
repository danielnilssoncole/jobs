from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Employer(models.Model):
	user = models.OneToOneField(User)
	company_Name = models.CharField(max_length=255, unique=True)
	field = models.CharField(max_length=255, null=True)
	size = models.IntegerField(null=True)
	location = models.CharField(max_length=255, null=True)
	website = models.URLField(blank=True)
	contact = models.EmailField(max_length=255, null=True)
	slug = models.SlugField()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.company_Name)
		super(Employer, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.company_Name
		
class Job(models.Model):
	employer = models.ForeignKey(Employer)
	title = models.CharField(max_length=255)
	location = models.CharField(max_length=255, null=True)
	salary = models.CharField(max_length=255, null=True)
	description = models.TextField(null=True)
	views = models.IntegerField(default=0)
	pub_datetime = models.DateTimeField(auto_now_add=True)
	pub_date = models.DateField(auto_now_add=True)
	updated_datetime = models.DateTimeField(auto_now=True)
	updated_date = models.DateField(auto_now=True)
	slug = models.SlugField()
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Job, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.title
		
class Applicant(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=255, null=True)
	last_name = models.CharField(max_length=255, null=True)
	location = models.CharField(max_length=255, null=True)
	#slug = models.SlugField()
	
	# def save(self, *args, **kwargs):
# 		self.slug = slugify(self.company_Name)
# 		super(Employer, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.last_name
	


