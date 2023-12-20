from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order, OrderPainting


# class OrderPaintingForm(forms.ModelForm):
#     class Meta:
#         model = OrderPainting
#         fields = '__all__'


class OrderPaintingInline(admin.TabularInline):
    model = OrderPainting
    autocomplete_fields = ['painting']
    # form = OrderPaintingForm
    fields = ('painting', 'display_sold', 'price')  # Добавляем поле sold для отображения
    readonly_fields = ('display_sold',)
    extra = 0

    @admin.display(description="Наличие")
    def display_sold(self, instance):
        # Return the sold status from the related Painting instance
        if not instance.painting:
            return None
        if instance.painting.sold:
            return 'Продано'
        else:
            return 'Не продано'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'status', 'email',
                    'address', 'postal_code', 'city']
    list_filter = ['created', 'status']
    list_editable = ['status']
    list_display_links = ['full_name']
    inlines = [OrderPaintingInline]
    search_fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    @admin.display(description="Наличие", ordering=('first_name'))
    def full_name(self, order: Order):
        return f'{order.first_name} {order.last_name}'
