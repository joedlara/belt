from __future__ import unicode_literals
from django.db import models
import re, bcrypt, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def reg(self, data):
		errors = [] #show user all errors
		#check that the first and lastname have more than 2 characters and are only letters (no numbers!)
		if len(data['fnom']) < 2:
			errors.append("First name must be at least two characters long.")
		if not data['fnom'].isalpha():
			errors.append("First name may only be letters.")

		if len(data['lnom']) < 2:
			errors.append("Last name must be at least two characters long.")
		if not data['lnom'].isalpha():
			errors.append("Last name may only be letters.")
			#check that email is present and valid
		if data['e_address'] == '':
			errors.append("Email may not be blank.")
		if not EMAIL_REGEX.match(data['e_address']):
			errors.append("Please enter valid email address.")
			#validate email uniqueness
		try:
			User.objects.get(email_address = data['e_address'])
			errors.append("Email is alraedy registered")

		except:
			pass
			#check password validation (>= 8 charaters)
			#pw and confirm match 
		if len(data['pass_word']) < 8:
			errors.append("Password must be at least 8 characters") 
		if data['pass_word'] != data['confirm_pass_word']:
			errors.append("Password does not match Confirm Password.")
			#pretend we dont have to validate the birthday yet
			#and we dont want to validate email uniqueness yet..
			#and that we dont wnat to create any users yet...
		if data['dob'] == '':
			errors.append("Birthday is required.")
		elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			errors.append("Birthday cannot be in the future.")

		if len(errors) == 0:
			#no errors
			print ('no errors')
			data['pass_word'] = bcrypt.hashpw(data['pass_word'].encode('utf-8'), bcrypt.gensalt())
			new_user = User.objects.create(f_name = data['fnom'], l_name = data['lnom'], email_address = data['e_address'], pw = data['pass_word'], birthday = data['dob'])
			return {
				'new': new_user, 
				'error_list': None
			}
		else: 
			# yes errors
			print('errors')
			return {
				'new': None,
				'error_list': errors
			}
	def log(self, log_data):
		errors = []
		#check if users account exits
		try:
			found_user = User.objects.get(email_address = log_data['e_mail'])
			if bcrypt.hashpw(log_data['p_word'].encode('utf-8'), found_user.pw.encode('utf-8')) != found_user.pw.encode('utf-8'):
				errors.append("Incorrect password.")
		except:
			#email does not exist in database
			errors.append("Email address is not registered.")

		if len(errors) == 0:
			#no errors
			return {
				'logged_user': found_user,
				'list_errors': None
			}

		else:
			#found errors
			return {
				'logged_user': None,
				'list_errors': errors
			}

class QuoteManager(models.Manager):

	def add(self, data):
		errors = []

		if len(data['quote']) < 3:
			errors.append("Quote by must be at least 3 characters.")

		if len(data['message']) < 10:
			errors.append("Message must be at least 10 characters.")

		if len(errors) == 0:
			#no errors
			# print ('no errors')
			new_quote = Quote.objects.create(quote = data['quote'], message = data['message'], user = data['user'])
			return {
				'quote_info': new_quote, 
				'more_error': None
			}
		else: 
			# yes errors
			print('errors')
			return {
				'quote_info': None,
				'more_error': errors
			}

class User(models.Model):
	f_name = models.CharField(max_length = 255)
	l_name = models.CharField(max_length = 255)
	email_address = models.CharField(max_length = 255)
	pw = models.CharField(max_length = 255)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Quote(models.Model):
	quote = models.CharField(max_length = 255)
	message = models.TextField()
	user = models.ForeignKey(User)
	objects = QuoteManager()

class Favorite(models.Model):
	user = models.ForeignKey(User, related_name = 'user_likes')
	quote = models.ForeignKey(Quote, related_name = 'quote_likes') 














		



