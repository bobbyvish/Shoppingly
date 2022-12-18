from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:id>',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:prod_id>', views.AddToCart, name='add-to-cart'),

    path('update_item/', views.UpdateItem, name="update_item"),

    path('buy/', views.buy_now, name='buy-now'),


    path('profile/', views.CustomerProfileViews.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),

    path('product/', views.product, name='product'),
    path('product/<str:cats>', views.product, name='product'),

    # ------------------------------register-login-logout---------------------

    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ------------------------------Password Change---------------------

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
         form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    # ------------------------------Password Reset---------------------

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
         form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    # ------------------------------Checkout---------------------
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.PaymentDone, name='paymentdone')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
