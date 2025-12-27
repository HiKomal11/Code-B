from django.db import models
from ckeditor.fields import RichTextField  

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  
    author = models.CharField(max_length=100, default="Admin")
    created_at = models.DateTimeField(auto_now_add=True, null=True)   
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



