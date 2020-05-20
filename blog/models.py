from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import Textarea
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.FileField( upload_to="posts", max_length=100)
    # content = models.ImageField( upload_to="posts", height_field=None, width_field=None, max_length=None)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    # approved_comment = models.BooleanField(default=False)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2})},
    }

    class Meta:
        ordering = ['-date_commented']

    def __str__(self):
        return self.content
        

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    
    
