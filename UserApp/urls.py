from django.urls import path
from UserApp.views import *
urlpatterns = [
    path('',index,name='index'),


    path('category/',category,name='category'),
    path('option/<int:id>',option,name='option'),
    path('dish/<int:id>',dish,name='dish'),
    path('add_to_cart/<int:id>',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('book_order/',book_order,name='book_order'),
    path('logout/',logoutPageView,name='logout-page'),
    path('order/',order,name='order'),
     path('login/',loginPageView,name='login-page'),
     path('signup/',signupPageView,name='signup-page'),
     path('rating/',rating,name="rating"),
     path('package/',packagePageView,name='package-page'),
    #EXTRAS
    path('invoice/<int:id>',generate_report,name='invoice'),


]
