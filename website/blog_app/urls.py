from django.urls import path

from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('about/', views.render_about_page, name='about'),
    path('contacts/', views.render_contacts_page, name='contacts'),
    path('faq/', views.render_faq_page, name='faq'),
    path('articles/create/', views.create_article_page, name='create'),
    path('articles/', views.render_articles_page, name='articles'),
    path('registration/', views.render_registration_page, name='registration'),
    path('authorization/', views.render_authorization_page, name='authorization'),
    path('articles/search/', views.search, name='search'),
    path('articles/<slug:slug>/', views.render_article_detail_page, name='article_detail'),
    path('profile/', views.render_profile_page, name='profile'),
    path('articles/<int:article_id>/<str:action>/', views.add_vote, name='add_vote'),
    path('articles/update/<slug:slug>/', views.UpdateArticle.as_view(), name='update'),
    path('articles/delete/<slug:slug>/', views.DeleteArticle.as_view(), name='delete'),
    path('quit/', views.render_logout_page, name='quit')
]
