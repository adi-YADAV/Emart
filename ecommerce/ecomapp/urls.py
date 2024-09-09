"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ecomapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('product',views.product),
    path('register',views.register),
    path('ulogin',views.ulogin),
    path('about',views.about),
    path('contact',views.contact),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sortfilter/<sv>',views.sortfilter),
    path('pricefilter',views.pricefilter),
    path('search',views.search),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.cart),
    path('updateqty/<u>/<cid>',views.updateqty),
    path('remove/<cid>',views.remove),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('history/<uid>',views.history),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)