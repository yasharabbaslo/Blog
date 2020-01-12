from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField()
    tags = TaggableManager()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year, self.publish.month, 
        self.publish.day, self.slug])

    

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, null=False)
    email = models.EmailField(null=False)
    body = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Newsletter(models.Model):
    email = models.EmailField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Message(models.Model):
    name = models.CharField(max_length=80, null=False)
    email = models.EmailField(null=False)
    subject = models.TextField(null=False)
    body = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
    