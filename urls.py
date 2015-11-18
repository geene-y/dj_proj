from django.conf.urls import url
from .views import News, Post, Wiki, WikiArticle, wishlist_form
urlpatterns = [
    url(r'^news/$', view=News.as_view(), name='post'),
    url(r'^news/page(?P<page>\d+)/$', News.as_view(), name='posts'),
    url(r'^post/(?P<pk>\d+)/$', view=Post.as_view(), name='article'),
    url(r'^wiki/$', view=Wiki.as_view(), name='wiki'),
    url(r'^wiki/(?P<section>\w+)/$', WikiArticle.as_view()),
    url(r'^wiki/(?P<section>\w+)/page(?P<page>\d+)/$', WikiArticle.as_view()),
    url(r'^wish_list/$', view=wishlist_form, name='wl')
]
