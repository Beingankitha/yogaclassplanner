from django.shortcuts import render,redirect,HttpResponse
from .models import WebsiteUser
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from passlib.hash import sha256_crypt
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
import uuid


def index(request):
		return render(request,"index.html")

def userregister(request):
		return render(request,"register.html")


def save_data(request):
    if request.method=="POST":
        email = request.POST["email"]
        fullname =request.POST["fullname"]
        gender =request.POST["gender"]
        Health_cond=request.POST["chk"]
        whoyouare = request.POST["whoyouare"]
        password = request.POST["pwd"]
        cpassword = request.POST["cpwd"]
        add1 = request.POST["first_line"]
        add2 = request.POST["second_line"]
        add3 = request.POST["third_line"]
        town = request.POST["post_town"]
        postcode = request.POST["postcode"]
        
        if add2 is not None:
            add = add1 +" "+ add2
        elif add3 is not None:
            add = add +" "+ add3
        elif town is not None:
            add = add +" "+ town
        elif postcode is not None:
            add = add +" "+ postcode

        data = WebsiteUser.objects.all().filter(email=email)

        if data:
            messages.error(request,"This email is already registered, Use Different Email ID.. !!")
            return redirect("/userlogin")
        elif password == cpassword :
            if Health_cond == "yes":
                Hinfo = request.POST["txtBox"]
            else:
                Hinfo = "N/A"

            password = sha256_crypt.encrypt(password)
            user=WebsiteUser(email=email,fullname=fullname,gender=gender,address = add, is_health=Health_cond, health_info = Hinfo, registered_as=whoyouare, password=password)
            user.is_active = False
            user.save()            
            current_site = get_current_site(request)
            mail_subject = 'Activate your Yoga account.'
            html_message = render_to_string("user_activate_email.html", {
                'user': fullname,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token':account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(mail_subject,html_message, to=[to_email])
            email.send()
            # recipient_list = [email, ]
            # email_from = settings.EMAIL_HOST_USER
            # send_mail( mail_subject, html_message, email_from, recipient_list )
            messages.success(request,"Register Sucessfully Completed")
            messages.error(request,"Please confirm your email address to complete the registration")
            return render(request,"login.html")
        else:
            messages.error(request,"Password and confirm Password mismatch..!!")
            return redirect("/userregister")
    else:
        messages.error(request,"Registration Fail")
        return redirect("/userregister")
        
def activate(request, uidb64, token):
    try:
        uuid = force_str(urlsafe_base64_decode(uidb64))
        user = WebsiteUser.objects.get(id=uuid)
    except(TypeError, ValueError, OverflowError, WebsiteUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        subject = 'welcome to Yoga Class Planner world'
        message = f'Hi {user.fullname}, thank you for to activate your account at in Yoga Class Planner. Now you can log in to your account...'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Thank you for your email confirmation. Now you can login your account.")
        return redirect("/userlogin")
    else:
        return HttpResponse('Activation link is invalid!')

# user login		
def userlogin(request):
		return render(request,"login.html")

def login_check(request):
    if request.method=="POST":
        email= request.POST["email"]
        password =request.POST["password"]
        data = WebsiteUser.objects.get(email=email)
        print(data)
        
        if data is not None: 
            if sha256_crypt.verify(password, data.password):
                if data.is_active:
                    if data.registered_as == "student":
                        request.session["useremail"]=data.email
                        request.session["username"]=data.fullname.title() # session strt
                        messages.success(request,"Login Sucessfully Completed")
                        return redirect("/studentdash")
                    if data.registered_as == "teacher":
                        request.session["useremail"]=email
                        request.session["username"]=data.fullname.title() # session strt
                        messages.success(request,"Login Sucessfully Completed")
                        context = {'data':data}
                        return redirect("/teacher/dashboard")
                else:
                    messages.warning(request,"Your account needs to be verified")
                    return redirect("/userlogin")
            else:
                messages.warning(request,"Login Fail")
                return redirect("/userlogin")

def studentdash(request):
    if request.session.get("username") is not None:
        return render(request,"studentdash.html")
    else:
        return redirect("/userlogin")

def teacherdash(request):
    if request.session.get("username") is not None:
        return render(request,"teacherdash.html")
    else:
        return redirect("/userlogin")


# user Logout
def logout1(request): 
    try:
        del request.session["username"] #session end
    except KeyError:
        pass
    messages.success(request,"Logout Sucessfully Completed")
    return redirect("/userlogin")

#membership
def membership(request):
    return render(request,"membership.html")


		