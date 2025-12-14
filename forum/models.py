from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class ForumThread(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Post(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(validators=[MinLengthValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} → {self.thread}"
