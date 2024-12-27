from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=200, null=False,blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    # date_created=datetime.now() 
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    img=models.ImageField(upload_to='pics',null=True,default=False,blank=True)

    ''' class TodoImage(models.Model):
        todo = models.ForeignKey('Todo', on_delete=models.CASCADE, related_name='images')
        img = models.ImageField(upload_to='pics')'''

    def __str__(self):
        return f'Blog {self.title},{self.id}'
