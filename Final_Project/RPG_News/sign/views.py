from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from .forms import SignupForm, CommonSignupForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string 
from .token import account_activation_token 
from django.contrib.auth.models import User 
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self,  request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'account/invalid_code.html')
            return redirect('/')


# def creatingOTP():
#     otp = ""
#     for i in range(11):
#         otp+= f'{random.randint(0,9)}'
#     return otp

# def sendEmail(email):
#     otp = creatingOTP()
#     send_mail(
#     'One Time Password',
#     f'Your OTP pin is {otp}',
#     settings.EMAIL_HOST_USER,
#     [email],
#     fail_silently=False,
#     )
#     return otp

 # Функция случайных номеров
# def random_str():
#     _str = '1234567890abcdefghijklmnopqrstuvwxyz'
#     return ''.join(random.choice(_str) for i in range(4))
 
# def email_send(request):
 
#     return render(request,'email_send.html')


# def send_email(request):
#     if request.method == 'GET':
#         try:
#             email = request.GET['email']
#         except:
#             email = ''
#             email_code = random_str()
#             Msg = 'Код подтверждения:' + email_code
#             send_mail(Msg, settings.email_from
#                   [email])
#         print(email_code)
#                  # Сохранить код подтверждения на сеанс в следующей операции, чтобы проверить
#         request.session['email_code'] = email_code
#         return HttpResponse('ok')
#     else:             
#         if request.POST.get('email_code') == request.session['email_code']:
#             return redirect('/info/')
#         else: 
#             return HttpResponse ('ошибка «Код подтверждения»')







# def usual_login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
#         return HttpResponse('получил')
        

# def login_with_code_view(request):
#     username = request.POST['username']
#     code = request.POST['code']
#     if OneTimeCode.objects.filter(code=code, user__username=username).exists():
#         login(request, User)
#     else:
#         return HttpResponse('ошибка')





def signup(request): 
    if request.method == 'POST': 
        form = SignupForm(request.POST) 
        if form.is_valid(): 
            # save form in the memory not in database 
            user = form.save(commit=False) 
            user.is_active = False 
            user.save() 
            # to get the domain of the current site 
            current_site = get_current_site(request) 
            mail_subject = 'Activation link has been sent to your email id' 
            message = render_to_string('acc_active_email.html', { 
                'user': user, 
                'domain': current_site.domain, 
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
                'token':account_activation_token.make_token(user), 
            }) 
            to_email = form.cleaned_data.get('email') 
            email = EmailMessage( 
                        mail_subject, message, to=[to_email] 
            ) 
            email.send() 
            return HttpResponse('Please confirm your email address to complete the registration') 
    else: 
        form = SignupForm() 
    return render(request, 'signup.html', {'form': form}) 

def activate(request, uidb64, token): 
    User = get_user_model() 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None 
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True 
        user.save() 
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.') 
    else: 
        return HttpResponse('Activation link is invalid!') 




class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/ind.html'


class BaseRegisterView(CreateView):
    model = User
    form_class = CommonSignupForm
    success_url = '/confirm/'

@login_required
def uprade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')