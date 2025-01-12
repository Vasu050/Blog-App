from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import random

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/blog/myblogs/')
    
    if request.method=='POST':

        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user_obj = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            user_obj = None
        if user_obj is not None:
          
            user = authenticate(request, username=user_obj.username, password=password)
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
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
                request.session['username'] = username
                request.session['password1'] = password1
                return send_otp(request)
                
        else:
            messages.error(request,"password is not matching")
            return redirect('register')
    else:
        return render(request,'register.html')
    
def send_otp(request):
    otp=random.randint(1000, 9999)
    otp_expiry=timezone.now() + timedelta(minutes=1)
    email = request.session.get('email')
    request.session['otp'] = otp
    request.session['otp_expiry'] = otp_expiry.isoformat()
    send_mail(
    "Registration Code",                 
    f"Thank you for registering with us!.Here is your One Time Password \n {otp}",
    "{vasujain050@gmail.com}",                 
    [email],                              
    fail_silently=False,
    )
    messages.success(request,"OTP sent successfully.Check your mail")
    return redirect('verify')

def verify(request):
    if request.method=='POST':
        otp1 = request.POST['otp1']
        otp2 = request.POST['otp2']
        otp3 = request.POST['otp3']
        otp4 = request.POST['otp4']
        user_otp = int(otp1+otp2+otp3+otp4)
        stored_otp = request.session.get('otp')
        otp_expiry_str = request.session.get('otp_expiry')
        otp_expiry = datetime.fromisoformat(otp_expiry_str) 

        if timezone.now() > otp_expiry:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            return redirect('verify')  

        if not user_otp == stored_otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify')
        else:

            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            email = request.session.get('email')
            username = request.session.get('username')
            password1 = request.session.get('password1')
            
            if password1:
                user = User.objects.create_user(password=password1, username=username, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, "User registered successfully")
                request.session.pop('otp', None)
                request.session.pop('otp_time', None)
                request.session.pop('first_name', None)
                request.session.pop('last_name', None)
                request.session.pop('email', None)
                request.session.pop('username', None)
                request.session.pop('password1', None)
                request.session.pop('otp', None)
                request.session.pop('otp_expiry', None)
                return redirect('/')
            else:
                return redirect('register')
    return render(request, 'verify.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
     
    user=request.user
    if request.method=='POST':
        try:
            user.first_name=request.POST.get('first_name')
            user.last_name=request.POST.get('last_name')
            email=request.POST.get('email')
            request.session['email'] = email

            if email==user.email:
                user.save()
                messages.error(request,"Profile Updated Successfully")
                return redirect('profile')
                
            
            if User.objects.filter(email=email).exclude(email=user.email).exists():
                messages.error(request,"Email aready exist")
                return redirect('profile')
            
            else:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(request.user)
                uid = urlsafe_base64_encode(force_bytes(request.user.pk))
                verification_link = request.build_absolute_uri(
                    f"/verify_email/{uid}/{token}/"
                )
                email_expiry=timezone.now() + timedelta(minutes=1)
                request.session['email_expiry'] = email_expiry.isoformat()
           
                send_mail(
                    'Verify Your Email Address',
                    f'Click the link to verify your email: {verification_link}',
                    'admin@example.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'A verification link has been sent to your new email address.')
                return redirect('profile') 
                
        except Exception as e:
            return f'error: {str(e)}'
    
    return render(request,'profile.html',{'user':user})

def verify_email(request,uid,token):
      
    uid = urlsafe_base64_decode(uid).decode()
    user = User.objects.get(pk=uid)
    email_expiry_str = request.session.get('email_expiry')
    email_expiry = datetime.fromisoformat(email_expiry_str) 

    if timezone.now() > email_expiry:
        messages.error(request, "OTP has expired. Please request a new OTP.")
        return redirect('profile') 
        
    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        messages.error(request, "Invalid verification link. Please try again.")
        return redirect('profile')
    
    email= request.session.get('email')
    user.email = email
    user.save()
    messages.success(request,"Your Profile Updated Successfully")
    return redirect('profile')

def delete(request):
    if not request.user.is_authenticated:  
        messages.error(request, 'Authentication Required')
        return redirect('/')
    
    user=request.user
    try:
        user = request.user
        user.delete()  
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('/') 
    except Exception as e:
        messages.error(request, f"Error deleting account: {str(e)}")
        return redirect('/profile/') 
        
