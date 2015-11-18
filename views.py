from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Article
from .models import Navigate
from .models import Section
from .models import Comment
from .models import Article_comment

from .forms import ContactForm
from .forms import SearchForm

# Create your views here.

items_per_page = 5


class News(ListView):
    """
    View of main page. Only news.
    extra context for header
    pagination by var 'items_per_page'
    """
    model = Article
    context_object_name = 'content'
    template_name = 'bible/posts.html'
    paginate_by = items_per_page

    def get_context_data(self, **kwargs):
        context = super(News, self).get_context_data(**kwargs)
        context['navigation'] = Navigate.objects.all()
        return context

    def get_queryset(self):
        return Article.objects.filter(section_id=1)


class Wiki(ListView):
    """
    View for dif sections in wiki section
    images, no pagination
    extra context for header
    """
    model = Section
    context_object_name = 'sections'
    template_name = 'bible/wiki.html'

    def get_queryset(self):
        qs = super(Wiki, self).get_queryset()
        return qs.filter(navigate_id=2)

    def get_context_data(self, **kwargs):
        context = super(Wiki, self).get_context_data(**kwargs)
        context['navigation'] = Navigate.objects.all()
        return context


class WikiArticle(News):
    """
    View with custom url.
    urls are assigned to each section inside of db, for dynamic url navigation
    extra context for header and url for correct url pagination
    """
    template_name = 'bible/wiki_posts.html'

    def get_queryset(self):
        return Article.objects.filter(section_id__url=self.kwargs['section'])

    def get_context_data(self, **kwargs):
        context = super(News, self).get_context_data(**kwargs)
        context['navigation'] = Navigate.objects.all()
        context['paginator_url'] = get_object_or_404(Section, url=self.kwargs['section'])
        return context


class Post(DetailView):
    """
    View for each single post
    extra context for sidebar (last 5 objects in same section)
    and for header
    comment context aint resolved yet
    """
    model = Article
    context_object_name = 'article'
    template_name = 'bible/post.html'

    def get_context_data(self, **kwargs):
        context = super(Post, self).get_context_data(**kwargs)
        context['navigation'] = Navigate.objects.all()
        section = get_object_or_404(Article, pk=self.kwargs['pk'])
        section = section.section_id
        section_content = Article.objects.filter(section_id=section)
        context['sidebar'] = section_content.exclude(pk=self.kwargs['pk'])[:5]
#        context['comment'] = Article_comment.objects.filter(article_id=self.kwargs['pk'])

        return context


def wishlist_form(request):
    """
    Form assigned to wish_list url
    for users can have some chat on this page
    2 required params title and message
    if same message exist post will be ignored
    """
    form = ContactForm(request.POST or None)
    if form.is_valid():
        title = form.cleaned_data['title']
        text = form.cleaned_data['message']
        Comment.objects.get_or_create(title=title, text=text)
    return render(request, 'bible/contact.html', {'form': form,
                                                  'navigation': Navigate.objects.all(),
                                                  'comments': Comment.objects.order_by('-pdate')})


def searchtool_form(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        search_request = form.cleaned_data['searchfield']
        content = Article.objects.filter(text__icontains=search_request)
