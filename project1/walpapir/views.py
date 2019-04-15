#For registration
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm
)
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

import os
import os.path

from .models import User, Photo



#プロジェクトで使用しているUserモデルを取得
User = get_user_model()
# Create your views here.


def home(request):
    homePhoto = Photo.objects.all()

    return render(request, 'walpapir/home1.html', {
        'photo':homePhoto,
    })

def mobile(request):
    mobilePhoto = Photo.objects.all()

    return render(request, 'walpapir/mobile.html', {
        'photo':mobilePhoto,
    })

def desktop(request):
    desktopPhoto = Photo.objects.all()

    return render(request, 'walpapir/desktop.html', {
        'photo':desktopPhoto,
    })

def how2use(request):
    return render(request, 'walpapir/how2use.html')

def prehome(request):
    return render(request, 'walpapir/prehome.html')

def page4post(request):

    #ログインしてないと入れない
    if not User.is_authenticated:
        return HttpResponseRedirect(reverse('walpapir:login'))

    if request.method=='GET':
        return render(request,'walpapir/page4Post.html')

    image=request.FILES['image']
    title=request.POST['title']
    mode=request.POST['radio']
    user_id=request.POST['user']

    user=User.objects.get(id=user_id)
    user.photo_set.create(image=image,title=title,mode=mode)

    return HttpResponseRedirect(reverse('walpapir:postdone'))#次に表示させるページの名前

def postDone(request):
    return render(request, 'walpapir/postDone.html')

#They are debug functions.

def user_d(request):
    user_photo = User.photo_set.all()
    return render(request, 'walpapir/user_d', {
        'photo': user_photo,
    })


def redeem_d(request):
    return render(request, 'walpapir/page4Redeem.html')

def userEdit_d(request):
    if request.method=="GET":
        return render(request, 'walpapir/userEdit_d.html')

    user_id =request.POST["id"]
    user=User.objects.get(id=user_id)

    if "image" in request.FILES:
        if user.profilepicture.name != "profile_image/180x120.jpeg":
            a=os.path.join(settings.MEDIA_ROOT,user.profilepicture.name)
            os.remove(a)

        user.profilepicture=request.FILES["image"]
        user.save()

    user_photo = Photo.objects.all()

    return render(request, 'walpapir/userPage.html', {
        'photo': user_photo,

    })

def userCreateComplete_d(request):
    return render(request, 'walpapir/user_create_complete_d.html')

#=========================

class Top(generic.TemplateView):
    template_name = 'walpapir/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'walpapir/page4Login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'walpapir/top.html'

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""

    template_name = 'walpapir/page4register.html' #ユーザー登録のためのページ
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('walpapir/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('walpapir/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('walpapir:signup_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'walpapir/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'walpapir/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

"""def registarUserName(request):
    lists = request.POST
    handle_name = lists["handle_name"]

    User.handle_name = handle_name

    return render(request, 'walpapir/user_create_done.html')
"""

photo=Photo.objects.all()
img=16
search=""
page_last=0

def search(request):
    global photo,img,search,page_last
    lists=request.GET
    search,page,select=lists["search"],int(lists["page"]),lists["select"]
    photo=Photo.objects.all()

    if(select=="0"):
        photo=photo.order_by("-time")
    elif(select=="1"):
        photo=photo.order_by("time")

    if search=="":
        page_last=int(photo.count()/img)+1
        return render(request,'walpapir/searchResults.html',{
            'photo':photo[0+(img*(page-1)):img+(img*(page-1))],
            'page':page,
            'search':search,
            'page_last':page_last,
            'count':photo.count(),
            'select':int(select),
        })

    j=search.split()

    for s in j:
        photo=photo.filter(title__contains=s)

    page_last=int(photo.count()/img)+1

    return render(request,'walpapir/searchResults.html',{
        'photo':photo[0+(img*(page-1)):img+(img*(page-1))],
        'page':page,
        'search':search,
        'page_last':page_last,
        'count':photo.count(),
    })

def ajax(request):
    global photo,img,search,page_last
    page=int(request.GET["page"])
    return HttpResponse(render(request,'walpapir/image.html',{'photo':photo[0+(img*(page-1)):img+(img*(page-1))],}))

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuer

class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'walpapir/userPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo"]=self.request.user.photo_set.all()
        return context

class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'walpapir/userEdit_d.html'

    def get_success_url(self):
        return resolve_url('userPage', pk=self.kwargs['pk'])



class ImageView(generic.TemplateView):
    template_name = 'walpapir/imageView.html'

    def get_context_data(self, **kwargs):

        context = super(ImageView, self).get_context_data(**kwargs)
        photo=Photo.objects.all()

        try:
            context['prev'] = photo.filter(id__lt=self.kwargs.get('pk')).order_by("-id")[0].id
        except:
            context['prev'] = -1

        context['photo'] = photo.filter(id__gte=self.kwargs.get('pk'))[0]

        try:
            context['next'] = photo.filter(id__gt=self.kwargs.get('pk'))[0].id
        except:
            context['next'] = -1
        return context

class ImageView_u(generic.TemplateView):
    template_name = 'walpapir/imageView.html'

    def get_context_data(self, **kwargs):

        context = super(ImageView_u, self).get_context_data(**kwargs)
        photo=self.request.user.photo_set.all()

        try:
            context['prev'] = photo.filter(id__lt=self.kwargs.get('pk')).order_by("-id")[0].id
        except:
            context['prev'] = -1

        context['photo'] = photo.filter(id__gte=self.kwargs.get('pk'))[0]

        try:
            context['next'] = photo.filter(id__gt=self.kwargs.get('pk'))[0].id
        except:
            context['next'] = -1
        return context
