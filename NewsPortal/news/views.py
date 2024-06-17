from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.core.exceptions import FieldError
from .forms import NewsSearchForm, NewsForm, PostForm
from .models import News, Post, Category
from django.contrib import messages

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('categories')
        category_id = self.request.GET.get('category')
        if (category_id):
            queryset = queryset.filter(categories__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class NewsDetailView(View):
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        user_subscribed = False

        if request.user.is_authenticated:
            first_category = news.categories.first()
            if first_category:
                user_subscribed = request.user in first_category.subscribers.all()

        context = {
            'news': news,
            'user_subscribed': user_subscribed,
        }
        return render(request, 'news/news_detail.html', context=context)

class NewsSearchListView(ListView):
    model = News
    template_name = 'news/news_search.html'
    context_object_name = 'search_results'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = NewsSearchForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            created_at = form.cleaned_data.get('created_at')
            try:
                if title:
                    queryset = queryset.filter(title__icontains=title)
                if author:
                    queryset = queryset.filter(author__username__icontains=author)
                if created_at:
                    queryset = queryset.filter(created_at__gte=created_at)
            except FieldError:
                queryset = News.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsSearchForm(self.request.GET)
        return context

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_news',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.change_news',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_news',)

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        user = request.user
        news_id = request.POST.get('news_id')

        if user in category.subscribers.all():
            messages.warning(request, f"Вы уже подписаны на категорию '{category.name}'!")
        else:
            category.subscribers.add(user)
            messages.success(request, f"Вы успешно подписались на категорию '{category.name}'!")

        if news_id:
            return redirect('news_detail', pk=news_id)
        else:
            return redirect('news_list')