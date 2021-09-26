from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orderlist/", views.orderlist, name="OrderList"),
    path("front/", views.front, name="front"),
    path("comingsoon/", views.comingsoon, name="comingsoon"),
    path("products/", views.products, name="products"),
    path("products2/", views.products2, name="products2"),
    path("desserts/", views.desserts, name="Desserts"),
    path("bestseller/", views.bestseller, name="BestSeller"),
    path("cakes/", views.cakes, name="cakes"),
    path("cookiesandbrownies/", views.cookiesandbrownies, name="CookiesandBrownies"),
    path("login/", views.login, name="Login"),
    path('logout/', views.user_logout, name='Logout'),
    path("register/", views.register, name="Register"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="Tracker"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("paymentfailed/", views.paymentfailed, name="PaymentFailed"),
    path("paymentsuccess/", views.paymentsuccess, name="PaymentSuccess"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
