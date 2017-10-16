from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote, Favorite
from django.contrib import messages
import logging


def index(request):
	return render(request, 'belty/index.html')

def register(request):
	context = {
	'fnom': request.POST['first_name'],
	'lnom': request.POST['last_name'],
	'e_address': request.POST['email'],
	'pass_word': request.POST['password'],
	'confirm_pass_word': request.POST['confirm'],
	'dob': request.POST['birthdate']
	}
	reg_results = User.objects.reg(context)
	
	if reg_results['new'] != None:
		#created new user
		#reg_results['new'] == new_user
		request.session['user_id'] = reg_results['new'].id
		request.session['user_fname'] = reg_results['new'].f_name
		request.session['user_lname'] = reg_results['new'].l_name
		
		return redirect('/welcome')

	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def success(request):
	if 'user_id' not in request.session:
		messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
		return redirect('/')

	quote_list = []
	others_list = []
	fav_list = Favorite.objects.filter(user=request.session['user_id'])
	for quote in Quote.objects.all():
		if quote.user.id == request.session['user_id']:
			quote_list.append(quote)
		else: 
			others_list.append(quote)

	context_2 = {
	'quote_list': quote_list,
	'others_list': others_list, 
	'fav_list': fav_list, 
	}
	return render(request, 'belty/welcome.html', context_2)

def login(request):
	p_data = {
		'e_mail': request.POST['email'],
		'p_word': request.POST['password'],
	}

	log_results = User.objects.log(p_data)

	if log_results['list_errors'] != None:
		#get errors
		for error in log_results['list_errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect('/')

	else: 
		request.session['user_id'] = log_results['logged_user'].id
		request.session['user_fname'] = log_results['logged_user'].f_name
		return redirect('/welcome')

def logout(request):
	request.session.clear()
	return redirect('/')

def add(request):
	context_1 = {
		'quote': request.POST['quote'],
		'message': request.POST['message'],
		'user': User.objects.get(id = request.session['user_id'])
		}

	results = Quote.objects.add(context_1)
	if results['more_error']:
		#get errors
		for error in results['more_error']:
			# print error
			messages.add_message(request, messages.ERROR, error)
		return redirect('/welcome')
	
	else:
		messages.add_message(request,messages.ERROR, "You posted a quote")
		return redirect('/welcome')

def dashboard(request, quote_id):
	quote_list = []
	others_list = [] 
	for quote in Quote.objects.filter(id = quote_id):
		if quote.user.id == request.session['user_id']:
			quote_list.append(quote)
		else: 
			others_list.append(quote)
	context_3 = {
	'quote_list': quote_list,
	'others_list': others_list, 

	}
	return render(request, 'belty/dashboard.html', context_3)
	
def fav_quote(request, quote_id):

	person = User.objects.get(id = request.session['user_id'])
	quotesss = Quote.objects.get(id = quote_id)
	fav_quote = Favorite.objects.create(user=person, quote=quotesss)

	return redirect('/welcome')

	
def home(request):
	return redirect('/welcome')

def remove_quote(request, quote_id):
	if request.method == "POST":
		a_quote = Quote.objects.get(id = quote_id)
		
		if a_quote.user.id == request.session['user_id']:
			
			a_quote.delete();
		else:
			messages.add_message(request, messages.ERROR, "You're not allowed to do that")
	return redirect('/welcome')


def remove_fav(request, fav_id):
	fav_del = Favorite.objects.get(id=fav_id)
	fav_del.delete()
	
	return redirect('/welcome')








