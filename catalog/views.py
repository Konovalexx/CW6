from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from catalog.models import Product
from catalog.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
import random

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все опубликованные продукты
        all_products = Product.objects.filter(is_published=True)

        # Проверяем наличие параметра в запросе для отображения только своих статей
        if self.request.GET.get('my_articles'):
            random_products = all_products.filter(created_by=self.request.user)
            remaining_products = []
        else:
            # Проверяем количество продуктов
            if all_products.count() < 3:
                random_products = all_products
                remaining_products = []
            else:
                # Получаем 3 случайных продукта
                random_products = random.sample(list(all_products), 3)
                # Получаем оставшиеся продукты, исключая случайные
                remaining_products = all_products.exclude(id__in=[product.id for product in random_products])

        context['random_products'] = random_products
        context['remaining_products'] = remaining_products  # Добавляем оставшиеся продукты в контекст

        # Добавляем продукты текущего пользователя
        if self.request.user.is_authenticated:
            context['my_products'] = all_products.filter(created_by=self.request.user)

        # Проверяем, является ли пользователь модератором
        context['is_moderator'] = self.request.user.groups.filter(name='Moderators').exists()

        return context

    def get_queryset(self):
        # Фильтруем только опубликованные товары
        return Product.objects.filter(is_published=True)

class DraftListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/draft_list.html'  # Убедитесь, что у вас есть этот шаблон
    context_object_name = 'drafts'

    def get_queryset(self):
        # Возвращаем неопубликованные продукты текущего пользователя
        return Product.objects.filter(is_published=False, created_by=self.request.user)

class ModerationListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/moderation_list.html'  # Убедитесь, что у вас есть этот шаблон
    context_object_name = 'products'

    def get_queryset(self):
        # Возвращаем все продукты для модерации
        return Product.objects.all()  # Здесь можно добавить фильтрацию, если нужно

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, является ли пользователь модератором
        if not request.user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("У вас нет прав для доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        product = self.get_object()
        product.views_count += 1
        product.save()
        return response

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        # Проверяем, имеет ли пользователь право редактировать продукт
        if product.created_by != user and not user.has_perm('catalog.can_change_product_description') and not user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете редактировать эту статью.")
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        # Проверяем, имеет ли пользователь право удалять продукт
        if product.created_by != user and not user.has_perm('catalog.can_delete_product') and not user.groups.filter(name='Moderators').exists():
            return HttpResponseForbidden("Вы не можете удалить эту статью.")
        return super().dispatch(request, *args, **kwargs)