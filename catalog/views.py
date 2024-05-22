from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.views import View
from django.core.exceptions import PermissionDenied

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Category, Blog, Version


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Доступные категории товаров'
    }

class AccessRightsMixinView(View):
    """Миксин ограничения доступа для неавторизованных пользователей"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('catalog:access_error')
        return super().dispatch(request, *args, **kwargs)

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
    """Контроллер просмотра списка продуктов"""
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset


class ProductDetailView(DetailView):
        """Контроллер просмотра отдельного продукта"""
        model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания продукта"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list_category')
    # success_url = reverse_lazy('catalog:product_list_category', kwargs={'pk': self.object.category.pk})

    login_url = '/users/register/'

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_list_category', kwargs={'pk': self.object.category.pk})

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования продукта"""
    model = Product
    form_class = ProductForm
    # success_url = reverse_lazy('catalog:product_list')
    success_url = reverse_lazy('catalog:product_list_category')

    login_url = '/users/register/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_list_category', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):  # формирование формсета с версиями продукта
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        # проверка наличия единственной активной версии у продукта
        active_versions = Version.objects.filter(product=self.object, is_active=True)
        if active_versions.count() > 1:
            form.add_error(None, 'Выберите только одну активную версию')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if (user.has_perm('catalog.can_edit_category') and user.has_perm('catalog.can_edit_description')
                and user.has_perm('catalog.can_change_published')):
            return ProductModeratorForm
        if user == self.object.owner:
            return ProductForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления продукта"""
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/register/'

class BlogCreateView(CreateView):
    model = Blog
    fields = ('name', 'content', 'is_published')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('name', 'content', 'is_published')
    # success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):

        return reverse('catalog:view', args=[self.kwargs.get('pk')])

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')














