from django.urls import path, include
from manageapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.BookView.as_view(), name='home'),
    path('bookdetail/<int:pk>/', views.BookDetailView.as_view(), name='bookdetail'),
    path('search/', views.search, name='search'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('rmviawishlist/<int:id>/', views.rmviawishlist, name='removefromwishlist'),
    path('tinymce/', include('tinymce.urls')),
    path('addbooks/', views.addbooks, name='addbook'),
    # path('addreview/', views.addreview, name='addreview'),
    
    
    
    
    
    
    
    
    ############# User Management Urls ############################
    path('user_login/', views.user_login, name='userlogin'),
    path('user_signup', views.user_signup, name='usersignup'),
    path('user_logout/', views.user_logout, name='userlogout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.password_change, name='passwordchange'),
    path('password_reset_request/', views.password_reset_request, name='passwordresetrequest'),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='passwordreset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
