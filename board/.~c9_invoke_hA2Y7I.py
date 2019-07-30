from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'board'
urlpatterns = [

    #path('signup/', views.signup.as_view(), name='signup'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',board.views.activate, name='activate'),
    path('', views.PostList.as_view(), name='home'),
    path('create/',views.PostCreate.as_view(),name="create"),
    # 각 영화 detail url(Read)
    path('detail/<int:pk>/',views.PostDetail.as_view(),name="detail"),
    # 영화를 수정할 url (Update)
    path('update/<int:pk>/',views.PostUpdate.as_view(),name="update"),
    # 영화를 제거할 url (Delete)
    path('delete/<int:pk>/',views.PostDelete.as_view(),name="delete"),
    
    path('detail/<int:post_pk>/invite/create/',views.InviteCreate.as_view(), name='invite_create'),
    # <a href="{% url 'board:invite_detail' post_pk=post.id invite_pk=invite.id %}">{{ invite.title }}</a>:{{ invite.description }}
    # path('detail/<int:post_pk>/invite/detail/<int:invite_pk>/',views.InviteDetail.as_view(), name='invite_detail'),
    path('invite/detail/<int:pk>/', views.InviteDetail.as_view(), name='invite_detail'),
    path('invite/update/<int:pk>/', views.InviteUpdate.as_view(), name='invite_update'),
    path('invite/delete/<int:pk>/', views.InviteDelete.as_view(), name='invite_delete'),

# 그냥 여기서 post로 Comment가 주어진다면, cbv에서 무언가를 하여라.

    path('invite/detail/<int:invite_pk>/comment/create/', views.CommentCreate.as_view(), name='comment_create'),
    # path('comment/update/<int:pk>', views.CommentDetail.as_view(), name='comment_update'),
    path('invite/detail/<int:invite_pk>/comment/delete/<int:comment_pk>', views.CommentDelete.as_view(), name='comment_delete'),
    
    # path('invite/detail/<int:invite_id>', views.invite_detail, name='invite-detail'),
    # path('invite/detail/comment/new/<int:comment_id>', views.comment_new, name='comment-new'),

    #여기부터 크롤링
    path('admi')
    path('/card', board.views.card, name = "card"),

]