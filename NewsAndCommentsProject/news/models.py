from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, db_column='rating')

    def update_rating(self):
        from_posts = 0
        from_comments = 0
        from_comments_to_posts = 0
        list_of_posts = list(self.post_set.all())
        for p in list_of_posts:
            from_posts = from_posts + p.rating
        list_of_comments = list(self.user.comment_set.all())
        for c in list_of_comments:
            from_comments = from_comments + c.rating
        list_of_posts = list(self.post_set.all())
        for p in list_of_posts:
            list_of_comments = list(p.comment_set.all())
            for c in list_of_comments:
                from_comments_to_posts = from_comments_to_posts + c.rating

        self.rating = from_posts*3 + from_comments + from_comments_to_posts
        self.save()

    def __str__(self):
        return self.user.username




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    article = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_news = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ManyToManyField("Category", through="PostCategory")

    def __str__(self):
        art = self.article
        date = self.create_time
        prev = self.preview()
        return f'{date} {art}: {prev}'


    def get_absolute_url(self):
        if self.is_news == True:
            return reverse('news_detail', args=[str(self.id)])
        else:
            return reverse('articles_detail', args=[str(self.id)])


    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        if len(self.text)>20:
            return f'{self.text[:20]}...'
        else:
            return f'{self.text}'


class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()
