from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('details/<int:design_id>/', HomeView.as_view(), name='details'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'), 
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:design_id>/', addtocart, name='add_to_cart'),
    path('decrement_cart/<int:design_id>/', decrement_cart, name='decrement_cart'),
    path('remove_from_cart/<int:design_id>/', remove_from_cart, name='remove_from_cart'),
    # path('create_order/', create_order, name='create_order'),
    # path('purchase_result/', purchase_result, name='purchase_result'),
    # path('razorpay_webhook/', razorpay_webhook, name='razorpay_webhook'),
    path("initiate-payment/", initiate_payment, name="initiate_payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-failed/", payment_failed, name="payment_failed"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
