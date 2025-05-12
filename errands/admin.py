from django.contrib import admin
from .models import Category, Errand, ErrandApplication, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Errand)
class ErrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'tasker', 'category', 'budget', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'client__username', 'tasker__username')
    ordering = ('-created_at',)
    raw_id_fields = ('client', 'tasker', 'category')

@admin.register(ErrandApplication)
class ErrandApplicationAdmin(admin.ModelAdmin):
    list_display = ('errand', 'tasker', 'proposed_budget', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('errand__title', 'tasker__username', 'proposal')
    ordering = ('-created_at',)
    raw_id_fields = ('errand', 'tasker')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('errand', 'reviewer', 'reviewed', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('errand__title', 'reviewer__username', 'reviewed__username', 'comment')
    ordering = ('-created_at',)
    raw_id_fields = ('errand', 'reviewer', 'reviewed')
