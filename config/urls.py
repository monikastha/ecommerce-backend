from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/admin/', include('adminperson.urls')),
    path('api/', include('product.urls')),
    path('api/users/', include('users.urls')),
    path("api/", include("staff.urls")),
    path('api/', include('adminlocation.urls')),
    path('api/productcategory/', include('productcategory.urls')),
    path('api/admin/', include('promotion.urls')),
    path('api/deliveryman/', include('deliveryman.urls')),
    path('api/seller/', include('seller.urls')),
    path('api/buyer/', include('Buyer.urls')),
    path('api/warehouse/', include('stock.urls')),
    path('api/', include('review.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
