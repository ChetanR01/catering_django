from django.contrib import admin
from UserApp.models import *
# Register your models here.

admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(DishIngredient)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Rating)
