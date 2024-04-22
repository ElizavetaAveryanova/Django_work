from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsPageView, CategoryListView, ProductListView, ProductDetailsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('<int:pk>/products/', ProductListView.as_view(), name='category_products'),
    path('<int:pk>/product/', ProductDetailsView.as_view(), name='product_description')
]
