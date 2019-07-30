from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from board.forms import PostSearchForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
#from .forms import SearchForm
# from django.template import loader, render_to_string
from .models import Post, Invite, Comment
from django.urls import reverse_lazy
from .parser import parse_activity
from .mysql import mysql
# 지원 새로 추가 
# username = email 로 하겠음 
# 회원가입 시 username(email), password1, password2, nickname을 입력하게 됨 

from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile

from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'], password=request.POST['password1'])
            
            user.is_active = False # 이메일 인증 받기 전 
            user.save()
            nickname = request.POST["nickname"]
            profile = Profile(user=user, nickname=nickname)
            profile.save()
            
            # 여기부터 이메일 인증 
            current_site = get_current(request) # request를 보낸 사이트를 알려주고 templates에 넘겨서 동적으로 url 접근 가능
            # localhost:8000
            message = render_to_string('acc_active_email.html', 						{
                'user': user,
                'domain': current_site.domain,
                'uid': 			urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user_email = user.username  # username을 email로 받기로 했으니까 
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
            # 이메일 인증 끝  
            
            auth.login(request, user)
            return redirect('home')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
	    username = request.POST['username']
	    password = request.POST['password']
	    user = auth.authenticate(request, username=username, password=password)
	    if user is not None:
	        auth.login(request, user)
	        return redirect('home')
	    else:
	        return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        
        auth.logout(request)
        return redirect('home')
    return render(request, 'signup.html')
#치헌오빠 example 구경할라고 만들었어욤 나중에 지우기   
def example(request):
    return render(request, 'example.html')

# home.view
class PostList(ListView, FormView):     # generic view mixin?
    model = Post
    template_name = 'home.html'
    form_class =  PostSearchForm
    paginate_by = 8 # 한 페이지에 4개만 보여주기 // 얘 해주면 page_obj , paginator가 자동으로 되는건가? A: ListView에는 pagenation 기능이 있따
    
    def setup(self,request, *args, **kwargs):
        super(PostList, self).setup(request,*args,**kwargs)
        parse_activity()
        
    # 검색
    def form_valid(self,form): # 값이 전달 됬을 경우
        
        title = '%s' %self.request.POST['title'] # 검색어 
        post_list = Post.objects.filter(
            Q(title__icontains=title) | Q(description__icontains=title) # Q 객체를 사용해서 검색한다. 
                # title,description 칼럼에 대소문자를 구분하지 않고 단어가 포함되어있는지 (icontains) 검사 
        ).distinct() #중복을 제거한다. 
        
        # paginator = Paginator(post_list, 4) # 한 post_list queryset에서 페이지에 4개만 보여주기
        # page = self.request.GET.get('page') # 페이지
        # posts = paginator.get_page(page)  # posts는 post_list에서 4개씩 paginator한것?
        
        context = {
            'post_list' : post_list,
            'word' : title,
            'form' : form,
            # 'posts' : posts,
        }
        
        return render(self.request, self.template_name, context)    # No redirection
        
    #pagination
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        posts = paginator.get_page(page)
        return context
    
class PostCreate(CreateView):
    model = Post
    fields =  '__all__'
    template_name = './post/post_form.html'
    success_url = reverse_lazy('board:home')
class PostDetail(DetailView):
    model = Post
    template_name = './post/post_detail.html'
    
class PostUpdate(UpdateView):
    model = Post
    fields =  '__all__'
    template_name = './post/post_form.html'
    success_url = reverse_lazy('board:home')
class PostDelete(DeleteView):
    model = Post
    template_name = './post/post_delete.html'
    success_url = reverse_lazy('board:home')
  
  
class InviteCreate(CreateView):
    model = Invite
    fields = ['title', 'description']
    template_name = './post/invite_form.html'
    success_url = reverse_lazy('board:home')
    
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.post_pk = get_object_or_404(Post, pk=kwargs['post_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overridden to add the ipsum relation to the `Lorem` instance.
        """
        form.instance.post = self.post_pk
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    
class InviteDetail(DetailView):
    model = Invite
    template_name = './post/invite_detail.html'


    # post_pk = "post_pk"
    # invite_pk = 'invite_pk'
    
    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     Overridden so we can make sure the `Ipsum` instance exists
    #     before going any further.
    #     """
    #     self.post_pk = get_object_or_404(Post, pk=kwargs['post_pk'])
    #     return super().dispatch(request, *args, **kwargs)
    
class InviteUpdate(UpdateView):
    model = Invite
    fields = ['title', 'description']
    template_name = './post/invite_form.html'
    success_url = reverse_lazy('board:home')
    
class InviteDelete(DeleteView):
    model = Invite
    template_name = './post/invite_delete.html'
    success_url = reverse_lazy('board:home')


class CommentCreate(CreateView):
    model = Comment
    fields = ['text',]
    success_url = ''
    def dispatch(self, request, *args, **kwargs):
        self.invite_pk = get_object_or_404(Invite, pk=kwargs['invite_pk'])
        self.success_url = reverse_lazy('board:invite_detail',kwargs={'pk':kwargs['invite_pk'] })
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.invite = self.invite_pk
        form.instance.author = self.request.user
        return super().form_valid(form)
    

        # return reverse_lazy('resource-view',
        #                     kwargs={'param': param},
        #                     current_app='myapp')
class CommentDelete(DeleteView):
    model = Comment

# def invite_detail(request, invite_id):

#     invite = get_object_or_404(Invite, pk=invite_id)

#     #만약 post일때만 댓글 입력에 관한 처리를 더한다.

#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         comment_form.instance.author_id = request.user.id
#         # 이거 뜻 모르겠음
#         comment_form.instance.invite_id = invite_id
#         if comment_form.is_valid():
#             comment = comment_form.save()
            
#     #models.py에서 document의 related_name을 comments로 해놓았다.

#     comment_form = CommentForm()
#     comments = invite.comments.all()

#     return render(request, 'post/invite_detail.html', {'object':invite, "comments":comments, "comment_form":comment_form})
 
#  def comment_new(request, pk):
#      if request.method == 'POST':
#          form = CommentForm(request,POST)
#          if form.is_valid():
#              #form.save()
#              comment = form.save(commit=False)
#              comment.post = Post.objects.get(pk=pk)
#              comment.save()
#              return redirect('main.views.post_detadil', pk)
#         else:
#             form = CommentForm()
#         return render(request, 'post_form.html',{
#             'form' : form
#         })

def home(request) :
    return render(request, 'home.html')

def activity_list(request) :
    parse_activity()
    my_list = Post.objects.all()
    return render(request, 'activity_list.html', {'my_list' : my_list})
    
# 검색 2
class SearchFormView(FormView): 
    template_name = 'search.html'
    form_class = PostSearchForm
    # def form_valid(self, form):  # This method is called when valid form data has been POSTed.
    #     return super(SearchFormView, self).form_valid(form)
    def form_valid(self,form): # 값이 전달 됬을 경우
        
        title = '%s' %self.request.POST['title'] # 검색어 
        post_list = Post.objects.filter(
            Q(title__icontains=title) | Q(description__icontains=title) # Q 객체를 사용해서 검색한다. 
                # title,description 칼럼에 대소문자를 구분하지 않고 단어가 포함되어있는지 (icontains) 검사 
        ).distinct() #중복을 제거한다. 
        
        context = {}
        context['post_list'] = post_list # 검색된 결과 리스트를 컨텍스트 변수에 담는다.
        context['word'] = title # 검색어 저장
        context['form'] = form # PostSerachForm 객체를 form에 저장
        
        return render(self.request, self.template_name, context)    # No redirection
        
def about(request) :
    return render(request, 'about.html')