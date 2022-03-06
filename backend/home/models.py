from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название поста')
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_posts/', blank=True, null=True)
    pub_date = models.DateField(auto_now=True)
    in_archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} из категории\'{self.blog_category.name}\''
