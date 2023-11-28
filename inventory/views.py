from django.db.models import QuerySet
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from inventory.models import Product, Sale, Analytics, Customer
from django.urls import reverse_lazy
from .forms import ProductForm, SaleForm, CustomerForm, EmailForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class ProductListView(ListView):
    """
    A view for displaying a paginated list of products.

    Attributes:
        model (Model): The Django model used for retrieving the list of products.
        template_name (str): The name of the template to be rendered.
        context_object_name (str): The name under which the list of products is available in the template context.
        paginate_by (int): The number of products to display per page in pagination.

    Methods:
        get_queryset(self) -> QuerySet:
            Returns the queryset of products to be displayed, using the custom method `get_all_stock()`.

        get_context_data(self, *, object_list=None, **kwargs) -> dict:
            Returns the context data for rendering the template. Adds the title 'List of Products' to the context.

    Example:
        To use this view, add the following URL pattern to your Django project's URLs:

        ```python
        path('products/', ProductListView.as_view(), name='product_list'),
        ```

    Note:
        This view assumes the existence of a custom model method `get_all_stock()` in the `Product` model.

    See Also:
        `ListView` documentation: https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#listview
    """

    model = Product
    template_name = 'inventories/product_index.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset of products to be displayed, using the custom method `get_all_stock()`.

        Returns:
            QuerySet: The queryset of products.

        See Also:
            `get_all_stock` method in the `Product` model.
        """
        return Product.objects.get_all_stock()

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Returns the context data for rendering the template. Adds the title 'List of Products' to the context.

        Args:
            object_list (list, optional): A list of objects to be used as the object_list attribute.
            kwargs (dict): Additional keyword arguments.

        Returns:
            dict: The context data.

        Example:
            ```python
            context = super().get_context_data(object_list=my_object_list, additional_data='extra')
            context['title'] = 'List of Products'
            return context
            ```
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Products'
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventories/product_detail.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Detail'
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'inventories/product_create.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'inventories/product_create.html'
    fields = '__all__'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventories/product_confirm_delete.html'
    success_url = reverse_lazy('product-index')
    context_object_name = 'product'


class SaleListView(ListView):
    model = Sale
    template_name = 'inventories/sale_index.html'
    context_object_name = 'sales'
    paginate_by = 10

    def get_queryset(self):
        return Sale.objects.get_all_sales()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = 'List of Sales'
        return context


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'inventories/sale_detail.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = 'Sales Details'
        return context


class SaleCreateView(CreateView):
    model = Sale
    template_name = 'inventories/sale_create.html'
    fields = '__all__'


class SaleUpdateView(UpdateView):
    model = Sale
    template_name = 'inventories/sale_create.html'
    fields = '__all__'


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'inventories/sale_confirm_delete.html'
    success_url = reverse_lazy('sale-index')
    context_object_name = 'sale'


class CustomerListView(ListView):
    model = Customer
    template_name = 'inventories/customer_index.html'
    context_object_name = 'customers'
    paginate_by = 15

    def get_queryset(self):
        return Customer.objects.get_all_customers()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = 'List of Customers'
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'inventories/customer_detail.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = 'Customer Details'
        return context


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'inventories/customer_create.html'
    fields = '__all__'


class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'inventories/customer_create.html'
    fields = '__all__'


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'inventories/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-index')
    context_object_name = 'customer'


class AnalyticListView(ListView):
    model = Analytics
    template_name = 'inventories/analytic_index.html'
    context_object_name = 'analytic'
    paginate_by = 5

    def get_queryset(self):
        return Analytics.objects.get_all_analysis()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analysis'] = 'List of All Analysis'
        return context


class AnalyticDetailView(DetailView):
    model = Analytics
    template_name = 'inventories/analytic_detail.html'
    context_object_name = 'analytic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['analysis'] = 'Detail of Analysis'
        return context


class SendEmailView(FormView):
    template_name = 'inventories/send_email.html'
    form_class = EmailForm
    success_url = reverse_lazy('product-index')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        recipient = form.cleaned_data['recipient']

        send_mail(subject, message, 'youremail@gmail.com', [recipient])
        messages.success(self.request, 'Email sent successfully')

        return super().form_valid(form)


def pie_chart(request):
    labels = []
    data = []

    queryset = Product.objects.all()
    for product in queryset:
        labels.append(product.name)
        data.append(product.quantity_on_hand)
        return render(request, "inventories/piechart.html",
                      {
                          'labels': labels,
                          'data': data

                      })


@login_required
def chart_view(request):
    pie_data = []  # Example data for the pie chart
    pie_labels = []

    bar_data = []  # Example data for the bar chart
    bar_labels = []
    queryset = Product.objects.all()
    total_products = Product.objects.count()
    total_quantity_on_hand = sum(product.quantity_on_hand for product in Product.objects.all())
    total_quantity_sold = sum(sale.quantity_sold for sale in Sale.objects.all())
    total_revenue_generated = sum(sale.product.unit_price * sale.quantity_sold for sale in Sale.objects.all())
    total_customers = Customer.objects.count()

    for product in queryset:
        pie_labels.append(product.name)
        pie_data.append(product.quantity_on_hand)
        bar_data.append(product.quantity_on_hand)
        bar_labels.append(product.name)

    context = {
        'pie_data': pie_data,
        'pie_labels': pie_labels,
        'bar_data': bar_data,
        'bar_labels': bar_labels,
        'total_products': total_products,
        'total_quantity_on_hand': total_quantity_on_hand,
        'total_quantity_sold': total_quantity_sold,
        'total_revenue_generated': total_revenue_generated,
        'total_customers': total_customers,
    }

    return render(request, 'inventories/piechart.html', context)


'''
def analysis_view(request):
    total_products = Product.objects.count()
    total_quantity_on_hand = sum(product.quantity_on_hand for product in Product.objects.all())
    total_quantity_sold = sum(sale.quantity_sold for sale in Sale.objects.all())
    total_revenue_generated = sum(sale.product.unit_price * sale.quantity_sold for sale in Sale.objects.all())
    total_customers = Customer.objects.count()

    context = {
        'total_products': total_products,
        'total_quantity_on_hand': total_quantity_on_hand,
        'total_quantity_sold': total_quantity_sold,
        'total_revenue_generated': total_revenue_generated,
        'total_customers': total_customers,
    }

    return render(request, 'inventories/analysis_dashboard.html', context)
'''
