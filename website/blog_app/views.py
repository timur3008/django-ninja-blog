from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from slugify import slugify
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm

def render_home_page(request):
    questions = models.FAQ.objects.all()
    slides = models.Slider.objects.all()
    articles = models.Article.objects.all()

    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'questions': questions,
        'slides': slides,
        'articles': articles
    }

    return render(request, 'blog_app/index.html', context)

def render_about_page(request):
    return render(request, 'blog_app/about.html')

def render_contacts_page(request):
    return render(request, 'blog_app/contacts.html')

def render_faq_page(request):
    questions = models.FAQ.objects.all()
    context = {
        'questions': questions
    }

    return render(request, 'blog_app/faq.html', context)

def render_articles_page(request):
    query_params = request.GET.get('category')

    categories = models.Category.objects.all()
    articles = models.Article.objects.all()

    if query_params:
        # category = models.Category.objects.get(slug=query_params)
        # articles = articles.filter(category=category)
        articles = articles.filter(category__slug=query_params)

    paginator = Paginator(articles, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles,
        'categories': categories,
        'category_query': query_params
    }

    return render(request, 'blog_app/articles.html', context)

def render_registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!!!')
            return redirect('authorization')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'blog_app/registration.html', context)

def render_authorization_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт!!!')
                return redirect('home')
            else:
                messages.error(request, 'Пользователь не найден!!!')
        else:
            messages.error(request, 'Введён неправильный логин или пароль!!!')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'blog_app/authorization.html', context)

def render_article_detail_page(request, slug):
    article = models.Article.objects.get(slug=slug)
    comments = models.Comment.objects.filter(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False) # говорим чтоб форма не сразу отпарвлялась на выполнение в базу
            form.article = article
            form.author = request.user
            form.save()
            messages.success(request, f'Комментарий добавлен успешно - {request.user}!!!')
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()

    if request.user.is_authenticated:
        is_viewed = models.ArticleCountView.objects.filter(
            article=article,
            user=request.user
        ).exists()
        
        if not is_viewed:
            obj = models.ArticleCountView.objects.create(
                article=article,
                user=request.user
            )
            article.views += 1
            article.save()

    try:
        article.likes
    except Exception as exc:
        models.Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as exc:
        models.Dislike.objects.create(article=article)

    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': comments.count()
    }

    return render(request, 'blog_app/article_detail.html', context)

@login_required(login_url='authorization')
def render_profile_page(request):
    articles = models.Article.objects.filter(author=request.user)
    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    total_comments = sum([article.comments.all().count() for article in articles])
    total_views = sum([article.views for article in articles])

    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': total_comments,
        'total_views': total_views
    }

    return render(request, 'blog_app/profile.html', context)

def render_logout_page(request):
    logout(request)
    messages.success(request, 'Вы вышли со своего аккаунта!!!')
    return redirect('home')

def create_article_page(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.slug = slugify(form.title)
            form.save()

            obj = models.Article.objects.get(pk=form.pk)
            for item in request.FILES.getlist('gallery'):
                article = models.ArticleImage.objects.create(
                    article=obj,
                    photo=item
                )
                article.save()

            messages.success(request, 'Статья успешно создана!!!')
            return redirect('article_detail', form.slug)
        else:
            messages.error(request, 'Данные введены неправильно. Попробуйте заново!!!')
    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'blog_app/article_form.html', context)

class UpdateArticle(UpdateView):
    model = models.Article
    # success_url = '/articles/' Article.get_absolute_url
    form_class = ArticleForm
    template_name = 'blog_app/article_form.html'

class DeleteArticle(DeleteView):
    model = models.Article
    success_url = '/articles/'
    template_name = 'blog_app/article_confirm_delete.html'

def add_vote(request, article_id, action):
    article = models.Article.objects.get(pk=article_id)

    user = request.user
    if action == 'add_like':
        if user in article.likes.user.all():
            article.likes.user.remove(user.pk)
        else:
            article.likes.user.add(user.pk)
            article.dislikes.user.remove(user.pk)
    else:
        if user in article.dislikes.user.all():
            article.dislikes.user.remove(user.pk)
        else:
            article.dislikes.user.add(user.pk)
            article.likes.user.remove(user.pk)
    
    return redirect('article_detail', slug=article.slug)

def search(request):
    query = request.GET.get('q')
    articles = models.Article.objects.filter(title__iregex=query)

    context = {
        'articles': articles,
        'total_articles': articles.count(),
        'query': query
    }

    return render(request, 'blog_app/search.html', context)