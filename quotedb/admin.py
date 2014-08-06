from django.contrib import admin
from quotedb.models import Quote, UserProfile, Comment

# Allow quotes, comments, and userProfiles to be modifiable from the admin panel
admin.site.register(Quote)
admin.site.register(Comment)

# User Profile Admin Configuration
class UserProfileAdmin(admin.ModelAdmin):
	fieldsets = [
		('User Information', {'fields': ['name', 'email', 'user_created']}),
		('Permissions', {'fields': ['is_moderator', 'is_admin']}),
		('Ban User', {'fields': ['is_banned']}),
		]
admin.site.register(UserProfile, UserProfileAdmin)
