from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, UsernameField, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from manageapp.models import User, Customer



class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        label = {'first_name':'First Name', 'last_name':'Last Name', 'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name':forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name':forms.TextInput(attrs={'class': 'form-control'}),
                   'email':forms.EmailInput(attrs={'class': 'form-control'})
                   }


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'city', 'zipcode']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.Select(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
                   }
        labels = {
            'locality':'Tole',
            'city':'Area',
        }
        
        
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
    )

        
        
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={"autofocus": True, 'class': 'form-control'}),
        required=True
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={"autofocus": True, 'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = get_user_model()
        # fields = ['newpassword1', 'newpassword2']
        
class PasswordResetForm(PasswordResetForm):
    
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = get_user_model
        fields = ['email']
        

    # captcha = 