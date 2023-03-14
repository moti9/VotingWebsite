from django.contrib import admin
from .models import EmailVerification
# Register your models here.
admin.site.site_header = "VotingApp Account Admin"
admin.site.site_title = "VotingApp Account Admin Panel"
admin.site.index_title = "Welcome to the VotingApp Account's Admin Panel"

admin.site.register(EmailVerification)
