from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsPageView, CategoryListView, ProductListView, ProductDetailView, BlogCreateView, \
    BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductCreateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    # path('<int:pk>/products/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/products/', ProductListView.as_view(), name='product_list_category'),

    path('create/', BlogCreateView.as_view(), name='create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]