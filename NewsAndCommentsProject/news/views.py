from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View,CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from django.core.mail import EmailMultiAlternatives
from .forms import PostForm
from django.template.loader import render_to_string
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

# class CreateNews(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
#     permission_required = ('news.add_post')
#     form_class = PostForm
#     model = Post
#     template_name = 'create_news.html'
class CreateNews(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = ('news.add_post')

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        to_html = {'categories': categories}
        return render(request, 'create_news.html', context=to_html)

    def post(self, request, *args, **kwargs):
        user_from = request.POST['user']
        user_from = User.objects.get(username= f'{user_from}')
        author_from = Author.objects.get(user=user_from)
        text_from = request.POST['text']
        name = request.POST['article']
        category = request.POST.getlist('category', ['category1'])
        new_post = Post(
            article = name,
            text = text_from,
            author = author_from
        )
        new_post.save()

        for cat in category:
            cat_from = Category.objects.get(name = cat)
            pc = PostCategory(
                post = new_post,
                category = cat_from
            )
            pc.save()

            subscribers = cat_from.author_set.all()
            for aut in subscribers:

                html_content = render_to_string(
                    'message.html',
                    {
                        'user': aut,
                        'category': cat,
                        'post': new_post
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'{cat_from.name}',
                    body=text_from,
                    from_email='viktorsung@yandex.ru',
                    to=[aut.user.email]
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()
        return redirect(f'http://127.0.0.1:8000/posts/news/{new_post.id}')


class CreateArticles(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        to_html = {'categories': categories}
        return render(request, 'create_article.html', context=to_html)

    def post(self, request, *args, **kwargs):
        user_from = request.POST['user']
        user_from = User.objects.get(username=f'{user_from}')
        author_from = Author.objects.get(user=user_from)
        text_from = request.POST['text']
        name = request.POST['article']
        category = request.POST.getlist('category', ['category1'])
        new_post = Post(
            article=name,
            text=text_from,
            author=author_from,
            is_news = False
        )
        new_post.save()

        for cat in category:
            cat_from = Category.objects.get(name=cat)
            pc = PostCategory(
                post=new_post,
                category=cat_from
            )
            pc.save()

            subscribers = cat_from.author_set.all()
            for aut in subscribers:
                html_content = render_to_string(
                    'message.html',
                    {
                        'user': aut,
                        'category': cat,
                        'post': new_post
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'{cat_from.name}',
                    body=text_from,
                    from_email='viktorsung@yandex.ru',
                    to=[aut.user.email]
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()
        return redirect(f'http://127.0.0.1:8000/posts/news/{new_post.id}')



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
        last_post = category_from.post_set.all().order_by('-create_time').first()
        subscriber = Subscribers(
            author = author_from,
            category = category_from
        )
        subscriber.save()
        message_to = f'Вы подписались на рассылку по категории {category_from.name}'

        html_content = render_to_string(
            'message.html',
            {
                'user': user_from,
                'category': category_from,
                'post': last_post
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{category_from.name}',
            body = message_to,
            from_email='viktorsung@yandex.ru',
            to = [user_from.email]
        )

        msg.attach_alternative(html_content,'text/html')
        msg.send()



        return redirect('/')





