from django.contrib import admin
from manageapp.models import User, Customer, Book, Cart, OrderedPlaced, Review, WishList, Profile
# Register your models here.

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(OrderedPlaced)
admin.site.register(Review)
admin.site.register(WishList)
admin.site.register(Profile)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
