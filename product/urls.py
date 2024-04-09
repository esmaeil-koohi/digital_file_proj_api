from . import views
from django.urls import path

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('files/', views.FileListView.as_view(), name='file-list'),
    path('files/<int:pk>', views.FileDetailView.as_view(), name='file-detail'),


    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),

    path('products/<int:product_id>/files/', views.FileListView.as_view(), name='file-list'),
    path('products/<int:product_id>/files/<int:pk>', views.FileDetailView.as_view(), name='file-detail')


]
