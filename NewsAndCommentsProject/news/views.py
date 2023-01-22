from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View,CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryList(LoginRequiredMixin, ListView):
    permission_required = ('news.add_post')
    model = Category
    ordering = 'id'
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class NewsList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(is_news = True) #super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'not_news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(is_news = False) #super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context




class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# def create_news(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         form.is_news = True
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'create_news.html', {'form': form})
#
# def create_article(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         form.is_news = False
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/articles/')
#     return render(request, 'create_article.html', {'form': form})

class CreateNews(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'

class CreateArticles(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'



class NewsUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'


class ArticleUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'


class NewsDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = ('news.add_post')
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')

class ArticleDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required = ('news.add_post')
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('article_list')


@login_required
def subs(request):
    user_req = request.POST['user']
    catetory_req = request.category
    Subscribers.objects.create(author = user_req, category = catetory_req)
    Subscribers.objects.create(author=user_req, category=catetory_req)
    return redirect('/')

class Subs(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        authors = Author.objects.all()


        to_html = {'categories': categories, 'authors': authors}
        return render(request, 'category.html', context=to_html)

    def post(self, request, *args, **kwargs):
        user_from = User.objects.get(username = request.POST['choose_author'])
        author_from = Author.objects.get(user = user_from)
        category_from = Category.objects.get(name =request.POST['choose_category'] )

        subscriber = Subscribers(
            author = author_from,
            category = category_from
        )
        subscriber.save()
        message_to = f'Вы подписались на рассылку по категории {category_from.name}'

        send_mail(
            subject=f'{category_from.name}',
            message = message_to,
            from_email='viktorsung@yandex.ru',
            recipient_list =[user_from.email]

        )

        return redirect('/')





