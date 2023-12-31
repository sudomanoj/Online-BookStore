from django.shortcuts import render, redirect
from django.http import HttpResponse
from manageapp.forms import LoginForm, SignupForm, CustomSetPasswordForm, PasswordResetForm
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
from manageapp.models import User, Cart, Customer, Book
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q


class BookView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        return render(request, 'manageapp/base.html', {'books':books})
    
class BookDetailView(LoginRequiredMixin, View):
    login_url = 'userlogin'
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        book_already_in_cart = False
        count = 0
        if request.user.is_authenticated:
            book_already_in_cart = Cart.objects.filter(Q(user=request.user) & Q(book=book.id)).exists()
            count = Cart.objects.filter(user=request.user).count()
            context = {
                'book':book,
                'book_already_in_cart':book_already_in_cart,
                'count':count
            }
        return render(request, 'manageapp/bookdetail.html', context=context)
    
def search(request):
    query = request.POST.get('search', '')
    book = None
    if query:
        book = Book.objects.filter(Q(genre__icontains=query))
    return render(request, 'manageapp/search_results.html', {'query':'query', 'book':book} )
        
 
 
 

































































####################### Authentication Related Work Starts From Here ################################

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
    

@login_required    
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('userlogin')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = CustomSetPasswordForm(user)
    return render(request, 'manageapp/password_change_form.html', {'form':form})
    

def password_reset_request(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=user_email)).first()
            if associated_user:
                mail_subject = 'Password reset request'
                message = render_to_string("manageapp/password_reset_template.html", 
                               {
                                   'user': associated_user,
                                   'domain': get_current_site(request).domain,
                                   'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                                   'token': account_activation_token.make_token(associated_user),
                                   'protocol': 'https' if request.is_secure() else 'http',
                                   }
                               )
                email = EmailMessage(mail_subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, f'{associated_user} Password reset link has been sent to your email!!')
                    return redirect('home')
                else:
                    messages.error(request, 'Problem while sending email!')

            else:
                return redirect('home')
    return render(request, 'manageapp/password_reset.html', {'form':form})

def passwordResetConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user.email)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed successfully!')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'manageapp/password_reset_confirm.html', {'form':form})
    else:
        messages.error(request, 'Activation link is invalid!')
    messages.error(request, 'Something went wrong, redirecting back to homepage')
    return redirect('home')
    