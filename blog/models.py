from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

def upload_to(instance,filename):
	username = instance.user.username
	return '%s/%s/%s'%('PostsFiles',username,filename)

class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title',max_length = 50, null=False, blank=False)
    content = RichTextField()
    image = models.ImageField(verbose_name='Post Image',upload_to=upload_to)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Created Date")
