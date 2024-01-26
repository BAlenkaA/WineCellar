from django.contrib import admin

from vine.models import Color, Vine, Category, Sweetness, Variety

admin.site.empty_value_display = 'Не задано'


@admin.register(Vine)
class VineAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'colors',
        'sweetness',
        'varieties_display',
        'factory',
        'year',
        'tasty',
        'tasting',
    )
    search_fields = (
        'title',
        'category',
        'colors',
        'sweetness',
        'factory',
    )
    list_filter = (
        'category',
        'colors',
        'sweetness',
        'factory',
        'year',
        'tasty',
        'tasting',
    )

    def varieties_display(self, obj):
        return ', '.join(variety.name for variety in obj.variety.all())
    varieties_display.short_description = 'Сорта винограда'


@admin.register(Category, Color, Sweetness, Variety)
class SimpleModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
