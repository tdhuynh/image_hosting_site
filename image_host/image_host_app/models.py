from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
    user = models.ForeignKey('auth.User')
    image = models.FileField()
    title = models.CharField(max_length=50)
    nsfw = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    @property
    def all_comments(self):
        return Comment.objects.filter(post=self)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"

    @property
    def get_next_post(self):
        next_post = Post.objects.filter(id__gt=self.id)
        if next_post:
            return next_post.first()
        return False

    @property
    def get_previous_post(self):
        prev_post = Post.objects.filter(id__lt=self.id).order_by('-id')
        if prev_post:
            return prev_post.first()
        return False


class Comment(models.Model):
    user = models.ForeignKey('auth.User')
    post = models.ForeignKey(Post)
    text = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField('auth.User')

    @property
    def user_posts(self):
        return Post.objects.filter(user=self.user)
