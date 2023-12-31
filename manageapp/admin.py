from django.contrib import admin
from manageapp.models import User, Customer, Book, Cart, OrderedPlaced
# Register your models here.

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(OrderedPlaced)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
