from django.contrib import admin, messages
from django.http import HttpResponseRedirect

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
    # list_editable = ['status']
    list_display_links = ['full_name']
    readonly_fields = ['status']
    inlines = [OrderPaintingInline]
    change_form_template = 'admin/orders/order/change_order.html'
    search_fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

    @admin.display(description="Наличие", ordering=('first_name'))
    def full_name(self, order: Order):
        return f'{order.first_name} {order.last_name}'

    # def save_model(self, request, order, form, change):
    #     order_paintings = order.order_paintings.all()
    #     if change:
    #         old_status = Order.objects.get(pk=order.pk).status
    #         if order.status == Order.Status.SUCCESS and old_status != Order.Status.SUCCESS:
    #             if any(op.painting.sold for op in order_paintings):
    #                 messages.set_level(request, messages.ERROR)
    #                 messages.error(request, "Одна или несколько картин в заказе уже проданы.")
    #                 return  # Stop the save operation
    #
    #             for op in order.order_paintings.all():
    #                 op.painting.sold = True
    #                 op.painting.save()
    #
    #         elif order.status != Order.Status.SUCCESS and old_status == Order.Status.SUCCESS:
    #             for op in order.order_paintings.all():
    #                 op.painting.sold = False
    #                 op.painting.save()
    #
    #     super().save_model(request, order, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if 'paid_button' in request.POST:
            self.paid_function(request, object_id)
            return HttpResponseRedirect(request.get_full_path())
        elif 'processed_button' in request.POST:
            self.processed_function(request, object_id)
            return HttpResponseRedirect(request.get_full_path())
        elif 'cancel_button' in request.POST:
            self.cancel_function(request, object_id)
            return HttpResponseRedirect(request.get_full_path())
        return super().change_view(request, object_id, form_url, extra_context)

    def paid_function(self, request, object_id):
        obj = self.get_object(request, object_id)
        order_paintings = obj.order_paintings.all()
        old_status = Order.objects.get(pk=obj.pk).status
        if old_status != Order.Status.SUCCESS:
            if any(op.painting.sold for op in order_paintings):
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Одна или несколько картин в заказе уже проданы.")
                return  # Stop the save operation

            for op in order_paintings:
                op.painting.sold = True
                op.painting.save()
        obj.status = Order.Status.SUCCESS
        OrderForm = self.get_form(request, obj, change=True)
        form = OrderForm(request.POST, request.FILES, instance=obj)
        super().save_model(request, obj, form, change=True)
        messages.success(request, 'Заказ оплачен')

    def processed_function(self, request, object_id):
        obj = self.get_object(request, object_id)
        order_paintings = obj.order_paintings.all()
        old_status = Order.objects.get(pk=obj.pk).status
        if old_status == Order.Status.SUCCESS:
            for op in order_paintings:
                op.painting.sold = False
                op.painting.save()
        obj.status = Order.Status.PROCESSED
        OrderForm = self.get_form(request, obj, change=True)
        form = OrderForm(request.POST, request.FILES, instance=obj)
        super().save_model(request, obj, form, change=True)
        messages.success(request, 'Заказ обработан')


    def cancel_function(self, request, object_id):
        obj = self.get_object(request, object_id)
        order_paintings = obj.order_paintings.all()
        old_status = Order.objects.get(pk=obj.pk).status
        if old_status == Order.Status.SUCCESS:
            for op in order_paintings:
                op.painting.sold = False
                op.painting.save()
        obj.status = Order.Status.CANCELED
        OrderForm = self.get_form(request, obj, change=True)
        form = OrderForm(request.POST, request.FILES, instance=obj)
        super().save_model(request, obj, form, change=True)
        messages.success(request, 'Заказ обработан')

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
