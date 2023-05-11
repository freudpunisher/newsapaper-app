from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Article
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

    # def process_request(self, request):
    #     if not request.user.is_authenticated:
    #         return redirect('login')


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_Detail.html'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body')
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def process_request(self):
        if self.request.status_code == '403':
            return redirect('article_list')
