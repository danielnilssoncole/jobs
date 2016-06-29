import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobs4.settings')

import django
django.setup()

from django.contrib.auth.models import User
from jobslist.models import Employer, Job, Applicant

def populate():
	u1 = add_user('user1', 'user1pass', 'user1@gmail.com')
	e1 = add_employer(u1, 'Employer 1', 'Engineering', '100', 'Tampa, FL', 
		'hr@employer1.com', 'https://www.google.com/')
	add_job(e1, 'Engineer', e1.location, '$80,000', 32)
	add_job(e1, 'Sales Person', e1.location, '$60,000', 16)
	
	u2 = add_user('user2', 'user2pass', 'user2@gmail.com')
	e2 = add_employer(u2, 'Employer 2', 'Marketing', '200', 'Orlando, FL', 
		'hr@employer2.com', 'https://www.google.com/')
	add_job(e2, 'Sales Representative', e2.location, '$70,000', 16)
	add_job(e2, 'Regional Manager', e2.location, '$90,000', 32)
	
	u3 = add_user('user3', 'user3pass', 'user3@gmail.com')
	e3 = add_employer(u3, 'Employer 3', 'Finance', '1000', 'New York, NY',
			'hr@employer3.com', 'https://www.google.com/')
	add_job(e3, 'Analyst', e3.location, '$90,000', 16)
	add_job(e3, 'Account Manager', e3.location, '$100,000', 32)
	
	u5 = add_user('user5', 'user5pass', 'user5@gmail.com')
	a5 = add_applicant(u5, 'Applicant', 'Five', 'Tampa, FL')
	
	u6 = add_user('user6', 'user6pass', 'user6@gmail.com')
	a6 = add_applicant(u6, 'Applicant', 'Six', 'Miami, FL')
	
	for e in Employer.objects.all():
		for j in Job.objects.filter(employer=e):
			print "- {0} - {1}".format(str(e), str(j))
			
	for a in Applicant.objects.all():
		print "- {0} {1} - {2}".format(a.first_name, a.last_name, a.user)
		

def add_user(username, password, email):
	u = User.objects.get_or_create(username=username, password=password)[0]
	u.set_password(password)
	u.email = email
	u.save()
	return u
	
def add_employer(user, company_Name, field, size, location, contact, website):
	e = Employer.objects.get_or_create(user=user, company_Name=company_Name)[0]
	e.field = field
	e.size = size
	e.location = location
	e.contact = contact
	e.website = website
	e.save()
	return e
	
def add_job(employer, title, location, salary, views):
	j = Job.objects.get_or_create(employer=employer, title=title)[0]
	j.location = location
	j.salary = salary
	j.views = views
	j.save()
	return j
	
def add_applicant(user, first_name, last_name, location):
	a = Applicant.objects.get_or_create(user=user)[0]
	a.first_name = first_name
	a.last_name = last_name
	a.location = location
	a.save()
	return a
	
	
if __name__ == '__main__':
    print "Starting jobslist population script..."
    populate()