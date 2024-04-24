from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Category, Blog


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Доступные категории товаров'
    }

class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            print(f'Имя - {name}\n'
                  f'Телефон - {phone}\n'
                  f'Сообщение: {message}')

        return render(request, 'catalog/contacts.html')


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Категория: {category_item.name}'
        return context_data



class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    extra_context = {
        'title': 'Описание товара'
    }

class BlogCreateView(CreateView):
    model = Blog
    fields = ('name', 'content')
    success_url = reverse_lazy('catalog:blog_list')

class BlogListView(ListView):
    model = Blog

class BlogDetailView(DetailView):
    model = Blog

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('name', 'content')
    success_url = reverse_lazy('catalog:blog_list')

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')











