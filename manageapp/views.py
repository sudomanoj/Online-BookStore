from django.shortcuts import render, redirect
from django.http import HttpResponse
from manageapp.forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from manageapp.tokens import account_activation_token
from manageapp.models import User
from django.contrib.auth import login, logout, authenticate


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'manageapp/base.html')
    
class BookListings(LoginRequiredMixin, View):
    login_url = 'user_login'
    def get(self, request, *args, **kwargs):
        return render(request, 'manageapp/base.html')
 
def user_login(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Form is not valid.')

        return render(request, 'manageapp/login.html', {'form': form})
    else:
        return redirect('home')

def activate(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=user_id)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified successfully!')
        return redirect('userlogin')   
    else:
        messages.error(request, 'Activation link invalid')
    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string("manageapp/account_activate_template.html", 
                               {
                                   'user': user.email,
                                   'domain': get_current_site(request).domain,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': account_activation_token.make_token(user),
                                   'protocol': 'https' if request.is_secure() else 'http',
                                   }
                               )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        # messages.success(request, f'Dear {user}, please go to your mail for email verification!')
        messages.success(request, f'{user} Your account created successfully!, check your email for verification process!!')
    else:
        messages.error(request, f'Problem sending email to {email}, check if you typed it correctly!')
        
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')  
    else:
        form = SignupForm()

    return render(request, 'manageapp/signup.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return HttpResponse('You must be loggedin first')