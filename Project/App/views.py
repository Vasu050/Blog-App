from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
# from .models import PasswordResetRequest
from django.core.mail import send_mail
# Create your views here.
def user_login(request):
    if request.method=='POST':
        '''username=request.POST['email']
        password=request.POST['password']'''
        
        
        '''try:
            user = User.objects.get(email=email)  
            if user.check_password(password):  
                auth.login(request, user) 
            user = authenticate(request, username=email, password=password)
                return redirect('blog/')  
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login') 
        except User.DoesNotExist:
            messages.info(request, 'User does not exist')
            return redirect('login') 
    else:
        return render(request, 'login.html')'''
        '''user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            return redirect('blog/blogs/')  
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/')  
    else:
        return render(request, 'login.html')'''
        

        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Find user by email
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            user = None
        if user is not None:
            # Authenticate using username and password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog/myblogs/')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('/')
        else:
            messages.info(request, 'User does not exist')
            return redirect('/')
    else:
        return render(request, 'login.html')
    
def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"email aready exist")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request,"username aready exist")
                return redirect("register")
            else:

                user=User.objects.create_user(password=password1,username=username,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,"user created")
                return redirect('/')
        else:
            messages.error(request,"password is not matching")
            return redirect('register')
    else:
        return render(request,'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

    
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Create reset request and generate token
            reset_request = PasswordResetRequest(user=user, email=email)
            reset_request.generate_token()
            reset_request.save()
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found.')

    return render(request, 'forgot-password.html')

def reset_password_view(request, token):
    # Check if the token is valid
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        # Set the new password
        user = reset_request.user
        user.set_password(new_password)
        user.save()

        # Mark the token as used
        reset_request.is_used = True
        reset_request.save()

        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})