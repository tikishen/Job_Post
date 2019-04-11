from django.contrib import admin
from foods.models import Food, Cafe, Meal, Category, Comment, Favorite

# Register your models here.
admin.site.register(Food)
admin.site.register(Cafe)
admin.site.register(Meal)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Favorite)
