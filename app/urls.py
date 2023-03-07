from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import *

urlpatterns = [


################### Authentication

    path("accounts/login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("registration/",
        views.CustomerRegistrationView.as_view(),
        name="customerregistration",
    ),
    path("changepassword/",
        auth_views.PasswordChangeView.as_view(
            template_name="app/changepassword.html",
            form_class=ChangePasswordForm,
            success_url="/passwordchangedone/",
        ),
        name="changepassword",
    ),
    path("passwordchangedone/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="app/passwordchangedone.html"
        ),
        name="passwordchangedone",
    ),
    path("password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="app/password_reset.html", form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),
    path("password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="app/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path("password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="app/password_reset_confirm.html",
            form_class=MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path("password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="app/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),


################### Home Page

    path("", views.home.as_view(), name="home"),
    path("search/", views.search, name="search"),


####################### product Detail

    path("product-detail/<int:pk>", views.product_detail.as_view(), name="product-detail"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("buy/", views.buy_now, name="buy-now"),


######################## Profile

    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),


######################## Cart

    path("cart/", views.show_cart, name= "showcart"),
    path("pluscart/",views.plus_cart),
    path("minuscart/",views.minus_cart),
    path("removecart/",views.remove_cart),


########################## CheckOut

    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    
########################### Ordered Products

    path("orders/", views.orders, name="orders"),
    
    
#################### Product Wise different Pages with Filtering

    path("mobile/", views.mobile, name="mobile"),
    path("mobile/<slug:data>", views.mobile, name="mobiledata"),
    
    path("laptop/", views.laptop, name="laptop"),
    path("laptop/<slug:data>", views.laptop, name="laptopdata"),
    
    path("topwear/", views.top_wear, name="topwear"),
    path("topwear/<data>", views.top_wear, name="topweardata"),
    
    path("bottomwear/", views.bottom_wear, name="bottomwear"),
    path("bottomwear/<data>", views.bottom_wear, name="bottomweardata"),
    
    path("wristwatch/", views.wrist_watch, name="wristwatch"),
    path("wristwatch/<data>", views.wrist_watch, name="wristwatchdata"),
    
    path("footwear/", views.foot_wear, name="footwear"),
    path("footwear/<data>", views.foot_wear, name="footweardata"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
