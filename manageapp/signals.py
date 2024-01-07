from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed, Signal
from django.dispatch import receiver
from manageapp.models import User, Profile
# from django.contrib.auth.models import User as u 

def login_success(sender, request, user, **kwargs):
    pass

user_logged_in.connect(login_success, sender=User)

@receiver(user_logged_out, sender=User)
def logout_success(sender, request, user, **kwargs):
    print('##############################')
    print('Logged-out Signal')
    print('Sender: ', sender)
    print('Request: ', request)
    print('User: ', user)
    print(f'Kwargs: {kwargs}')
    
@receiver(user_login_failed)
def login_failed(sender, request, credentials, **kwargs):
    try:
        user= User.objects.get(email=credentials.get('username'))
        profile_instance, profile_created = Profile.objects.get_or_create(person=user)
        profile_instance = user.profile
        profile_instance.login_failure_count += 1
        profile_instance.save()

    
        if profile_instance.login_failure_count >= 10:
            user.is_active = False
            user.save()
            print(f'User {user.email} has been blocked')
    except:
        print(f"No such user {credentials.get('username')}")