from django.contrib import admin
from django.urls import path
from store import views
from .auth import auth_middleware
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [

    path('', views.index, name = 'index'),
    path('insert', views.insert, name = 'insert'),
    path('deldata/<str:pk>', views.deldata, name = 'deldata'),
    path('update/<str:pk>', views.update, name = 'update'),
    path('p_details/<str:pk>', views.p_details, name = 'p_details'),
    path('about', views.about, name = 'about'),
    path('cart', views.cart, name = 'cart'),
    path('orders', views.orders, name = 'orders'),
    # path('checkout', views.checkout, name = 'checkout'),
    path('checkout', auth_middleware(views.checkout), name = 'checkout'),
    path('confirmation', views.confirmation, name = 'confirmation'),
    path('contact', views.contact, name = 'contact'),
    path('elements', views.elements, name = 'elements'),
    path('main', views.main, name = 'main'),
    path('product_details', views.product_details, name = 'product_details'),
    path('shop', views.shop, name = 'shop'),
    path('signup', views.signup, name = 'signup'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('check', views.check, name = 'check'),
    path('pdfinvoice', views.pdfinvoice, name = 'pdfinvoice'),
    path('ordemail', views.ordemail, name = 'ordemail'),
    path('invoice', views.invoice, name = 'invoice'),
    path('contact_us', views.contact_us, name = 'contact_us'),
    path('change_password/<str:pk>', views.change_password, name = 'change_password'),
    path('create_invoice', views.create_invoice, name = 'create_invoice'),
    path('userprofile/<str:pk>',views.userprofile, name = 'userprofile'),
    # path('signup', views.handlesignup, name = 'handlesignup'),
    # path('login', views.handleLogin, name = 'handleLogin'),
]