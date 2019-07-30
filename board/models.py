from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 200, verbose_name = '검색어')     # verbose_name = 모델 필드 custom
    description = models.TextField(max_length=4000)
    company = models.URLField()
    created_at = models.CharField(max_length = 20)
    image = models.CharField(max_length = 200)
    # view = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Invite(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(max_length=4000)
    post = models.ForeignKey(Post, related_name='invites',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='invites',on_delete=models.CASCADE)

class Comment(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # like = models.IntegerField(default=0)
    # dislike = models.IntegerField(default=0)

    # def __str__(self):
    #     return (self.author.username if self.author else "무명")+ "의 댓글"
        
        
    
# class Reply(models.Model):
#     message = models.TextField(max_length=4000)
#     invite = models.ForeignKey(Invite, related_name='replys',on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True)
#     created_by = models.ForeignKey(User, related_name='replys',on_delete=models.CASCADE)

#     def __str__(self):

#         return self.message[:10]


# 여기부터 크롤링입니다

# 지원
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(max_length=10)
