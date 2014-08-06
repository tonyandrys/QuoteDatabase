from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Profile should never be created manually! Create a standard User (Django auth) and this will be created automatically.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	is_banned = models.BooleanField(default=False)
	is_moderator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	elephants = models.IntegerField(default=0)
	
	# On creation of a User, create a UserProfile
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(user=instance)
	post_save.connect(create_user_profile, sender=User)
		
	def __unicode__(self):
		return self.name

class Quote(models.Model):
	text = models.CharField(max_length=5000)
	author = models.ForeignKey(UserProfile)
	rating = models.IntegerField(default=0)
	pub_date = models.DateTimeField('date published')
	
	def __unicode__(self):
		return "Quote: "+self.text[0:21]+"..."

class Comment(models.Model):
	quote = models.ForeignKey(Quote)
	author = models.ForeignKey(UserProfile)
	text = models.CharField(max_length=500)

	def __unicode__(self):
		return "Comment: "+self.text[0:21]+"..."

class IPBan(models.Model):
	ip_address = models.CharField(max_length=15)

class Vote(models.Model):
	quote = models.ForeignKey(Quote)
	user = models.ForeignKey(UserProfile)
	rating_change = models.IntegerField()

	def __unicode__(self):
		return "Quote ID: " + str(self.quote.id) + " | " + str(self.rating_change)
