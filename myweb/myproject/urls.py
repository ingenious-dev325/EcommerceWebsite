from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("front/", views.front, name="front"),
    path("comingsoon/", views.comingsoon, name="comingsoon"),
    path("products/", views.products, name="products"),
    path("products2/", views.products2, name="products2"),
    path("boxoffour/", views.boxoffour, name="BoxOfFour"),
    path("login/", views.login, name="Login"),
    path('logout/', views.user_logout, name='Logout'),
    path("register/", views.register, name="Register"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="Tracker"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("boxcheckout/", views.boxcheckout, name="BoxCheckout"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]
