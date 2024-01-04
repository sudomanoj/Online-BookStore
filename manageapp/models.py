from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from manageapp.managers import UserManager
from tinymce.models import HTMLField

################# Custom User Model ##################
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


CITY_CHOICES = (
    ('Butwal Devinagar', 'Butwal Devinagar'),
    ('Butwal Golpark', 'Butwal Golpark'),
    ('Butwal Buspark', 'Butwal Buspark'),
    ('Butwal Sukkhanagar', 'Butwal Sukkhanagar'),
    ('Butwal Yogikuti', 'Butwal Yogikuti'),
    ('Butwal Belbas', 'Butwal Belbas'),
    ('Butwal Tamnagar', 'Butwal Tamnagar'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    city = models.CharField(choices=CITY_CHOICES, max_length=50)
    
    def __str__(self):
        return str(self.name)   

genre_choices = (
    ('Historical Fiction', 'Historical Fiction'),
    ('Mystery', 'Mystery'),
    ('Sciende Fiction', 'Science Fiction'),
    ('Horror', 'Horror'),
    ('Romance', 'Romance'),
    ('Thriller', 'Thriller'),
)
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    genre = models.CharField(choices=genre_choices, max_length=50)
    description = HTMLField()
    book_image = models.ImageField(upload_to='booksimage')
    book_pdf = models.FileField(upload_to='bookspdf', blank=True, null=True)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.email
    
    @property
    def total_cost(self):
        return self.quantity * self.book.discounted_price
    

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delevered'),
    ('Cancel', 'Cancel'),
)

class OrderedPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price   


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i,i) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.book.title}"
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f" WishList For {self.user.email}"
    