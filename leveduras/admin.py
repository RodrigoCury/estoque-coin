from django.contrib import admin
from .models import Yeast, Brand, FermentativeProfile, Todo

# Register your models here.


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('activity', "user",)
    list_filter = ('activity', "user")
    raw_id_fields = ("user", )
    search_fields = ('activity',)


@admin.register(Yeast)
class YeastAdmin(admin.ModelAdmin):
    list_display = ('name', "user", 'reinnoculation_count',
                    'next_reinnoculation_limit_date')
    list_filter = ('name', "created_at", "user")
    date_hierarchy = "last_reinnoculation"
    raw_id_fields = ("user", )
    search_fields = ('name', "brand", 'fermentative_profile')
    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    readonly_fields = ('related_yeasts', 'visualize_img', )
    search_fields = ('name', "brand", 'fermentative_profile')
    prepopulated_fields = {
        "slug": ("name",)
    }

    def related_yeasts(self, obj):
        return [yeast.name for yeast in obj.get_yeasts_by_brand.all()]
    related_yeasts.short_description = 'Leveduras da marca'
    related_yeasts.allow_tags = True

    def visualize_img(self, obj):
        return obj.view_image

    visualize_img.short_description = "Imagem Cadastrada"
    visualize_img.allow_tags = True


@admin.register(FermentativeProfile)
class FermentativeProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    readonly_fields = ('related_yeasts', )
    search_fields = ('name', "brand", 'fermentative_profile')
    prepopulated_fields = {
        "slug": ("name",)
    }

    def related_yeasts(self, obj):
        return [yeast.name for yeast in obj.get_yeasts_by_profile.all()]
    related_yeasts.short_description = 'Leveduras da marca'
    related_yeasts.allow_tags = True
