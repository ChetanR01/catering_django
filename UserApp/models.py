from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Users(AbstractUser):
    full_name = models.CharField(max_length=100,null=True, blank=True,default="")
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    role = models.CharField(max_length=100,null=True, blank=True,choices=(('Staff','Staff'),('User','User')),default="User")
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="CategoryImages/", null=True, blank=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="OptionImages/", null=True, blank=True)

    def __str__(self):
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Dish(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="DishImages/", null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='DishIngredient')
    # For thali 
    is_thali = models.BooleanField(default=False)
    thali_tag_line = models.CharField(max_length=200, default='')
    thali_items = models.TextField( default='')

    def __str__(self):
        return self.name
    
class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_used = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.dish.name} {self.ingredient.name} {self.quantity_used}"

    
class CartItem(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)    
    in_cart = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)

    
class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=100,null=True, blank=True)
    items = models.ManyToManyField(CartItem)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    guest_count = models.IntegerField(default=1)
    venue = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100,default="Pending",null=True,blank=True)


    def clear_cart(self):
        for cart_item in self.items.all():
            cart_item.in_cart = False
            cart_item.save()

    def update_inventory(self):
        # Update the inventory based on the ingredients used in the order
        for cart_item in self.items.all():
            dish = cart_item.dish
            for dish_ingredient in dish.dishingredient_set.all():
                ingredient = dish_ingredient.ingredient
                quantity_used = int(dish_ingredient.quantity_used) * int(self.guest_count)
                ingredient.quantity -= int(quantity_used)
                ingredient.save()

class Rating(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    rate = models.IntegerField(null=True,blank=True,default=1)