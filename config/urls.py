from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('api/admin/', include('adminperson.urls')),
    path('api/products/', include('productcategory.urls')),
    path('api/users/', include('users.urls')),
    path("api/", include("staff.urls")),
    
]