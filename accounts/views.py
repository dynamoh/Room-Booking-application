from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404

from .models import User
from .forms import RegisterForm
from .tokens import account_activation_token
from rooms.models import Customer,Manager
# Create your views here.



def login_user(request):
    logout(request)
    email = password = ''
    val=0
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        obj = User.objects.filter(email=email).first()
        if obj!=None:
            if obj.is_active is False:
                val=2
            if user is not None:
                if user.is_active:
                    login(request, user)
                    obj = Customer.objects.filter(customer_id=request.user).first()
                    obj1 = Manager.objects.filter(manager_id=request.user).first()
                    if obj:
                        if obj.contact == '':
                            return HttpResponseRedirect('/')
                    return HttpResponseRedirect('/')
                else:
                    val=2
            else:
                val=1
                return render(request,'login.html',{'error':'Please Enter correct username and password !!','val':val})
        else:
            val=1
            return render(request,'login.html',{'error':'Please Enter correct username and password !!','val':val})

    return render(request,'login.html',{'error':'Please Enter correct username and password !!','val':val})


def signup_success(request):
    return render(request,'signup_successful.html')

def signup_failure(request):
    return render(request,'signup_failure_page.html')

def activated(request):
    return render(request,'activated.html')

def not_activated(request):
    return render(request,'not_activated.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST)
        email_check = request.POST.get('email')
        obj = User.objects.filter(email=email_check).first()
        if obj:
            return render(request,'signup_failure_page.html',{'message':'This Email has already been taken!!'})
        if form.is_valid():
            desig = request.POST.get('desig')

            user = form.save(commit=False)
            print("aagaya")
            user.is_active = False
            user.set_password(form.cleaned_data.get('password'))
            if desig == 'customer':
                user.manager = False
                user.customer= True
            else:
                user.manager = True
                user.customer= False
            user.save()
            user.refresh_from_db()
            current_site = get_current_site(request)
            mail_subject = '[noreply] Activate your Account'
            msg = 'Thanks for signing up, welcome to Room Booking. We are always ready to Welcome You.'
            message = render_to_string('acc_email_active.html', {
                'user': user,
                'domain': current_site.domain,
                'msg':msg,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return redirect('signup_success_page')
        else:
            return render(request,'signup_failure_page.html',{'message':'You have not been registered. Your Passwords doesnt match!!'})
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form,'done':0})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        if user.customer == True:
            obj = Customer.objects.create(customer_id=user,avatar='dummy.png')
        else:
            obj = Manager.objects.create(manager_id=user,avatar='dummy.png')
            user.is_active=False
        obj.save()
        # return redirect('home')
        return redirect('activatedpage')
    else:
        return redirect('not_activatedpage')
