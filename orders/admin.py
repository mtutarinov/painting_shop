from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from .models import Order, OrderPainting

class OrderPaintingForm(forms.ModelForm):
    sold = forms.BooleanField(required=False)  # Добавляем поле для редактирования

    class Meta:
        model = OrderPainting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderPaintingForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.painting_id:
            self.fields['sold'].initial = self.instance.painting.sold

    def save(self, commit=True):
        instance = super(OrderPaintingForm, self).save(commit=False)
        if instance.painting_id:
            painting = instance.painting
            painting.sold = self.cleaned_data['sold']
            painting.save()
        if commit:
            instance.save()
        return instance

class OrderPaintingInline(admin.TabularInline):
    model = OrderPainting
    autocomplete_fields = ['painting']
    form = OrderPaintingForm
    fields = ['painting', 'sold', 'price']  # Добавляем поле sold для отображения
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city',
                    'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderPaintingInline]
