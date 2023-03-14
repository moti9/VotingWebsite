from django.shortcuts import render,redirect
from polls.models import Contact
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def home(request):
    if request.method=="POST" and request.user.is_authenticated:
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        try:
            user=User(request.user)
            contact=Contact(user=user.id,name=name,email=email,subject=subject,message=message)
            contact.save()
        except ValidationError:
            return redirect('accounts:login')        
    return render(request, 'home.html')
