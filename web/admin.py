from django.contrib import admin
from .models import User, Membership, UserMembership, Subscription

admin.site.register(User)
admin.site.register(UserMembership)
admin.site.register(Membership)
admin.site.register(Subscription)
