# models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(default='Hola, LLEYO', max_length=100)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
                                    .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
                                    .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers_count(self):
        return Relationship.objects.filter(to_user=self.user).count()

    @staticmethod
    def get_recent_users():
        recent_users = User.objects.all().order_by('-date_joined')[:5]
        return recent_users

    @staticmethod
    def get_users_ordered_by_followers():
        # Obtener usuarios ordenados por la cantidad de seguidores
        users_ordered_by_followers = User.objects.annotate(follower_count=Count('related_to')).order_by('-follower_count')
        return users_ordered_by_followers



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True, verbose_name='Video')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text

    def Cantidad_likes(self):
        return self.likes.count()

class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} comenta en {self.post}"

    class Meta:
        ordering = ['-created_at']

class SocialComment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    social_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='social_comments')
