from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.urlresolvers import reverse
from quotedb.models import Quote, UserProfile, Comment, Vote
from random import randint

# Views for the QuoteDB App

# Displays database counts and other misc info
def status(request):
	# Get counts 
	quote_count = Quote.objects.count()
	user_count = UserProfile.objects.count()
	comment_count = Comment.objects.count()
	return render(request, 'quotedb/status.html', {'counts': {'quote': quote_count, 'user': user_count, 'comment': comment_count}})

def login_page(request):
	return render(request, 'quotedb/login.html')

def register_page(request):
	return render(request, 'quotedb/register.html')

def process_registration(request):
	# Retrieve new account credentials
	new_username = request.POST['username']
	new_email = request.POST['email']
	new_password = request.POST['password']
	new_password_c = request.POST['password_confirm']
	
	# Ensure all fields are filled
	if not (new_username and new_email and new_password and new_password_c):
		return HttpResponse("All fields must be filled to register an account.")
	
	# Ensure passwords match
	elif not (new_password == new_password_c):
		return HttpResponse("Passwords don't match.")
	
	# If data is valid, create the account and authenticate
	else:
		# Create a user in underlying auth framework
		u = User.objects.create_user(new_username, new_email, new_password)
		u.save()

		# Login using new account information
		user = authenticate(username=new_username, password=new_password)
		login(request, user)

		return render(request, 'quotedb/registration_successful.html', {'user_profile': u.get_profile()})

def process_login(request):
	# Retrieve submitted username and password
	user_input = request.POST['username']
	password_input = request.POST['password']
	
	# If username or password are blank, go back and display an error message
	if not (user_input or password_input):
		error_message = "You must enter both a username and a password."
		return HttpResponse(error_message)
	
	else: 
		# Attempt to authenticate using these credentials
		user = authenticate(username=user_input, password=password_input)

	# If credentials are valid, log the user into auth framework
	if user is not None:
		login(request, user)
		# Redirect to success page
		return HttpResponse("User " + user.get_username() + " logged in!")
	else:
		# If invalid credentails are passed, display an error message.
		error_message = "Invalid login credentials."
		return HttpResponse(error_message)

# Logs the current user out of the auth framework, wiping the local session data
@login_required
def logout_user(request):
	logout(request)
	return HttpResponse("You have been logged out.")

# Quote display page (should include comments soon)
def quote(request, quote_id):
	
	# Get the quote to display
	q = get_object_or_404(Quote, pk=quote_id)
	
	# Get the current path for redirect purposes
	next = request.get_full_path()

	# Get all comments associated with this quote
	comment_list = Comment.objects.filter(quote=q)

	return render(request, 'quotedb/view_quote.html', {'quote': q, 'comment_list': comment_list, 'next': next})

# View that displays a quote submission form for a user to fill out. Does NOT handle actual submission process.
@login_required
def new_quote_submit(request):
	return render(request, 'quotedb/add_quote.html')

# Performs the quote submission process, updates DB, and redirects user to their new quote
@login_required
def add_quote(request):
	
	# Try to retrieve the passed quote text to this page
	quote_text = request.POST['quote_text']
	
	# If we got no data, throw an error
	if (len(quote_text) == 0):
		return render(request, 'quotedb/add_quote.html', {
			'error_message': "Uh, quotes can't be blank."
		})
	
	# If we did get data, ensure it is within the size constraints defined by the model
	elif (len(quote_text) > 5000):
		# Redisplay the submission page
		return render(request, 'quotedb/add_quote.html', {
			'error_message': "Your quote is longer than 5000 characters. Quotes longer than this are not allowed at this time."
		})
	else:
	
		# Get the currently logged in user's profile
		u = UserProfile.objects.get(user_id__exact=request.user.id)
		
		# Get the current time to set published date/time of this Quote
		time = timezone.now()
		
		# Add this new quote to the database
		new_quote = Quote(text=quote_text, author=u, rating=0, pub_date=time)
		new_quote.save()

		# Redirect to the new Quote's page
		return HttpResponseRedirect(reverse('quotedb:quote', args=(new_quote.id,)))

# Displays all quotes in the system and provides links to their specific page for comments
def browse(request):
	
	# Get list of all Quotes in the system
	quote_list = Quote.objects.all();
	
	# Get the current path for redirecting
	next = request.get_full_path()

	# Pass them to the template as a context
	return render(request, 'quotedb/browse_quotes.html', {'quote_list': quote_list, 'next': next})

# User info page
@login_required
def user(request, user_id):
	user_profile = get_object_or_404(UserProfile, pk=user_id)
	return render(request, 'quotedb/user_info.html', {'user_profile': user_profile})

# Picks a random quote and redirects the browser to that quote's page (qdb/view)
def random(request):
	# Get a random number from [1,quotecount]
	quote_count = Quote.objects.count()
	r = randint(1,quote_count)

	# Redirect to qdb/view/random - HACK
	return HttpResponseRedirect('../'+str(r))
	# return redirect('quotedb.views.quote', quote_id=r)

# Triggers an vote on a quote. This method does no user validation, only ensures the the quote_id and vote_tag are within valid parameters.
@login_required
def vote(request, quote_id, vote_tag):
	# Ensure vote_tag is in valid range
	if (0 <= int(vote_tag) <= 1):
		
		# Get the quote requested and modify its rating.
		q = get_object_or_404(Quote, pk=quote_id)
		if (int(vote_tag) == 0):
			q.rating -= 1
			r_change = -1
		elif (int(vote_tag) == 1):
			q.rating += 1
			r_change = 1
		q.save()
	
	# Create a Vote object and write it to the database
	u = UserProfile.objects.get(user_id__exact=request.user.id)
	vote = Vote(quote=q, user=u, rating_change=r_change)
	vote.save()

	# Get the page to redirect
	redirect = str(request.GET['next'])

	# Finally, redirect back to the quote's view page
	return HttpResponseRedirect(redirect)

@login_required
def add_comment(request, quote_id):	
	# Get the quote to attach this comment to
	q = get_object_or_404(Quote, pk=quote_id)

	# Build Comment using passed text
	quote_text = request.POST['comment']
	
	# Get the UserProfile of the currently logged in user
	u = UserProfile.objects.get(user_id__exact=request.user.id)
	
	# Create and store the new Comment
	comment = Comment(quote=q, author=u, text=quote_text)
	comment.save()
	
	# Redirect to the previous page
	return HttpResponseRedirect(reverse('quotedb:quote', args=(q.id,)))	

@login_required
def shop(request):
	return render(request, 'quotedb/view_shop.html')

@login_required
def admin_panel(request):
	return render(request, 'quotedb/admin_panel.html')

@login_required
def ban_user(request, user_id):
	# Get the user to ban
	u = get_object_or_404(UserProfile, pk=user_id)

	# Ban their ass and strip any privileges they might have
	u.is_admin = False
	u.is_moderator = False
	u.is_banned = True
	u.save()
	return redirect('/qdb/user/' + user_id)

@login_required
def ip_ban(request, ip_address):
	# Add an IP Ban to the ban table
	ip_ban = IPBan(ip_address)
	ip_ban.save()
	return redirect('qdb/admin')
