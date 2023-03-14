from .models import *
from django.contrib import admin

# Register your models here.
admin.site.site_header = "VotingApp Polls Admin"
admin.site.site_title = "VotingApp Polls Admin Panel"
admin.site.index_title = "Welcome to the VotingApp Polls Admin Panel"


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Result)
admin.site.register(Contact)
