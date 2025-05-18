from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.text import slugify

class Slider(models.Model):
    title = models.CharField(max_length=40, verbose_name='Заголовок', default='')
    description = models.TextField(verbose_name='Описание', default='')
    image = models.ImageField(upload_to='slider/', verbose_name='Фото', default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

class FAQ(models.Model):
    question = models.TextField(verbose_name='Вопрос', default='')
    answer = models.TextField(verbose_name='Ответ', default='')

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = 'Вопрос и Ответ'
        verbose_name_plural = 'Вопросы и Ответы'

class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', help_text='Данное поле заполняется автоматически')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True, blank=True)
    preview = models.ImageField(upload_to='articles/previews/', null=True, blank=True, verbose_name='Превью')
    views = models.PositiveIntegerField(default=0, verbose_name='Кол-во просмотров')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='Автор')

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class ArticleImage(models.Model):
    photo = models.ImageField(upload_to='article/gallery/', verbose_name='Фото')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='gallery')

    class Meta:
        verbose_name = 'Картина'
        verbose_name_plural = 'Картинки'

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='all_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='all_views')

class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')
