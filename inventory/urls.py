from django.urls import path
from inventory import views

urlpatterns = [

    path('', views.ProductListView.as_view(), name='product-index'),

    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),

    path('products/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),

    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('sales/', views.SaleListView.as_view(), name='sale-index'),

    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),

    path('sales/create/', views.SaleCreateView.as_view(), name='sale-create'),

    path('sales/<int:pk>/update', views.SaleUpdateView.as_view(), name='sale-update'),

    path('sales/<int:pk>/delete/', views.SaleDeleteView.as_view(), name='sale-delete'),

    path('customers/', views.CustomerListView.as_view(), name='customer-index'),

    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),

    path('customers/create/', views.CustomerCreateView.as_view(), name='customer-create'),

    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer-update'),

    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),

    path('analysis/', views.AnalyticListView.as_view(), name='analytic-index'),

    path('analysis/<int:pk>/', views.AnalyticDetailView.as_view(), name='analytic-detail'),

    path('send_email/', views.SendEmailView.as_view(), name='send_email'),

    path('analysis/pie_chart/', views.chart_view, name='pie_chart'),

    path('products/pdf/', views.ProductPDFView.as_view(), name='products_pdf'),
]
