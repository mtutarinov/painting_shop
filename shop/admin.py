from django.contrib import admin
from .models import Category, Painting
from django.db.models.functions import Lower

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Painting)
class AdminPainting(admin.ModelAdmin):
    class PriceListFilter(admin.SimpleListFilter):
        title = 'Категория цен'
        parameter_name = 'price'

        def lookups(self, request, model_admin):
            return (
                ('low', 'Низкая цена'),
                ('medium', 'Средняя цена'),
                ('hight', 'Высокая цена')
            )

        def queryset(self, request, queryset):
            if self.value() == 'low':
                return queryset.filter(price__lte=2000)
            elif self.value() == 'medium':
                return queryset.filter(price__gt=2000, price__lte=10000)
            elif self.value() == 'hight':
                return queryset.filter(price__gt=10000)

    list_display = ['name', 'price', 'available']
    list_filter = [PriceListFilter, ('category', admin.RelatedOnlyFieldListFilter)]
    list_editable = ['price', 'available']
    search_fields = ['name__icontains']
    search_help_text = 'Поиск по названию картины'
    show_full_result_count = False
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    actions_on_bottom = True
    actions = ('not_available',)

    @admin.action(description='Нет в наличии')
    def not_available(self, request, queryset):
        queryset.update(available=False)


@admin.action(description='Снять с публикации')
def not_available(painting: AdminPainting, request, queryset):
    f = queryset.update(available=False)
    f.save()
