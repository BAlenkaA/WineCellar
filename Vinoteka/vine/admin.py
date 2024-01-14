from django.contrib import admin

from vine.models import Color, Vine, Category, Sweetness, Variety

admin.site.empty_value_display = 'Не задано'


class VineInline(admin.StackedInline):
    model = Vine
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        VineInline,
    )
    list_display = (
        'name',
        'description',
    )
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class SweetnessAdmin(admin.ModelAdmin):
    inlines = (
        VineInline,
    )


class ColorAdmin(admin.ModelAdmin):
    inlines = (
        VineInline,
    )


class VarietyAdmin(admin.ModelAdmin):
    inlines = (
        VineInline,
    )


class VineAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'colors',
        'variety',
        'sweetness',
        'year',
        'factory',
        'image',
        'tasty'
    )
    search_fields = ('title',)
    list_filter = ('tasty', 'date_create')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Sweetness, SweetnessAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Variety, VarietyAdmin)
admin.site.register(Vine, VineAdmin)
admin.site.empty_value_display = 'Не задано'
