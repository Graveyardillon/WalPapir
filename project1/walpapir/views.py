#For registration
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest,HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views import generic
from .forms import (
    LoginForm, UserCreateForm
)

from django.shortcuts import render





from .models import Photo
#プロジェクトで使用しているUserモデルを取得
User = get_user_model()



# Create your views here.
def home(request):
    return render(request, 'walpapir/home1.html')

def mobile(request):
    return render(request, 'walpapir/mobile.html')

def desktop(request):
    return render(request, 'walpapir/desktop.html')

def how2use(request):
    return render(request, 'walpapir/how2use.html')

def page4post(request):
    """
    if request.method=='GET':
        return render(request,'walpapir/page4Post.html')
    
    user = #login-user-models
       
    image=request.FILES['image']
    title=request.POST['title']
    mode=request.POST['radio']

    user.photo_set.create(image=image,title=title,mode=mode)

    return HttpResponseRedirect(reverse(''))#次に表示させるページの名前
    """
    return render(request, 'walpapir/page4post.html')

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


photo=Photo.objects.all()
img=4
search=""
page_last=0

def search(request):
    global photo,img,search,page_last
    lists=request.GET
    search,page=lists["search"],int(lists["page"])
    
    
    

    if search=="":
        page_last=int(photo.count()/img)+1
        return render(request,'walpapir/searchResults.html',{
            'photo':photo[0+(img*(page-1)):img+(img*(page-1))],
            'page':page,
            'search':search,
            'page_last':page_last,
            'count':photo.count(),
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

