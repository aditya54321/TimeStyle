from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('details/<int:design_id>/', details_view, name='details'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'), 
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:design_id>/', addtocart, name='add_to_cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)