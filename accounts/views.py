from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import EmailVerification
from django.conf import settings
import secrets


def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, "Hey, you're already loggedin.", extra_tags="alert alert-warning alert-dismissible fade show")
        return redirect("polls:home")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                user = User(username=username)
                verified = EmailVerification(user=user)
                # print(verified)
                if verified.is_active:
                    login(request, user)
                else:
                    messages.error(request,"Please activate your account.", extra_tags="alert alert-primary alert-dismissible fade show")
                    return redirect('accounts:verify_email')
            redirect_url = request.GET.get('next', 'polls:home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!",
                           extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request):
    if request.user.is_authenticated:
        messages.error(request, "Hey, you're already loggedin.", extra_tags="alert alert-warning alert-dismissible fade show")
        return redirect("home")
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password did not match!',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists!',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Email already registered!',
                               extra_tags='alert alert-warning alert-dismissible fade show')

            if check1 or check2 or check3:
                messages.error(
                    request, "Registration Failed!", extra_tags='alert alert-danger alert-dismissible fade show')
                return redirect('accounts:register')
            else:
                # mailStart
                # try:
                #     htmly = get_template('accounts/email.html')
                #     d = {'username': username}
                #     subject, from_email, to = 'Welcome to VotingApp', 'your_email@gmail.com', email
                #     html_content = htmly.render(d)
                #     msg = EmailMultiAlternatives(
                #         subject, html_content, from_email, [to])
                #     msg.attach_alternative(html_content, "text/html")
                #     msg.send()
                # except:
                #     pass
                #######
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                try:
                    # user = User.objects.get(email=email)
                    verification, created = EmailVerification.objects.get_or_create(user=user)
                    if created:
                        verification.is_active = True
                        code = str(secrets.randbelow(10**8))
                        verification.code = code
                        verification.save()
                    if not verification.is_active:
                        verification.is_active = True
                        verification.save()
                    # verification = EmailVerification(user=user)
                    # verification.save()
                    subject = 'Email Verification Code'
                    message = f'Your email verification code is: {verification.code}'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, from_email, recipient_list)
                    # return redirect('accounts:verify_email')
                    # mailEnd
                    messages.success(
                        request, f'Thanks for registering {user.username}.', extra_tags='alert alert-success alert-dismissible fade show')
                    return redirect('accounts:verify_email')
                except Exception:
                    messages.error(request,"Oops !! some error occured, please try again", extra_tags="alert alert-danger alert-dismissible fade show")
                    return redirect("accounts:register")
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"User with this email does not exist.", extra_tags="alert alert-danger alert-dismissible fade show")
            return redirect("accounts:send_verification_code")
        verification, created = EmailVerification.objects.get_or_create(user=user)
        if created:
            verification.is_active = True
            code = str(secrets.randbelow(10**8))
            verification.code = code
            verification.save()
            
        if not verification.is_active:
            verification.is_active = True
            verification.save()
            
        subject = 'VotingApp Email Verification Code'
        message = f'Please verify your account to use VotingApp. Your email verification code is: {verification.code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        # send_mail(subject, message, from_email, recipient_list)
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            messages.error(request,"Oops!! Please try again.", extra_tags="alert alert-danger alert-dismissible fade show")
            return redirect("accounts:send_verification_code")
        return redirect('accounts:verify_email')
    else:
        return render(request, 'accounts/send_verification_code.html')


def verify_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        code = request.POST['code']
        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.get(user=user, code=code)
        except User.DoesNotExist:
            messages.error(request,"User with this email does not exist.", extra_tags="alert alert-danger alert-dismissible fade show")
            return redirect('accounts:verify_email')

        except EmailVerification.DoesNotExist:
            messages.error(request,"Sorry, some error occured.", extra_tags="alert alert-danger alert-dismissible fade show")
            return redirect('accounts:verify_email')
        if verification.is_active:
            verification.is_active = False
            verification.save()
            user.is_active = True
            user.save()
            login(request, user)
        else:
            messages.error(request,"Sorry your code is invalid.", extra_tags="alert alert-danger alert-dismissible fade show")
            return redirect("accounts:send_verification_code")
        return redirect('home')
    else:
        pass
        # email_verification = EmailVerification.objects.get(user=request.user)
        # email_verification = EmailVerification.objects.get(user=user)
        email_verification = EmailVerification()

        return render(request, 'accounts/verify_email.html', {'email_verification': email_verification})

###############################################################
#################@DUMP-AREA-STARTED@###########################
###############################################################


# def send_verification_code(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request,"User with this email does not exist.", extra_tags="alert alert-danger alert-dismissible fade show")
#             return redirect("accounts:send_verification_code")
#         verification = EmailVerification(user=user)
#         if verification != None:
#             verification.is_active=False
#             # code = secrets.token_urlsafe(24)
#             code = str(secrets.randbelow(10**8))
#             verification.code = code
#         verification.save()
#         subject = 'Email Verification Code'
#         message = f'Your email verification code is: {verification.code}'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [email]
#         send_mail(subject, message, from_email, recipient_list)
#         return redirect('accounts:verify_email')
#     else:
#         return render(request, 'accounts/send_verification_code.html')