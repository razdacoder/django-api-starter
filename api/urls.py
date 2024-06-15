from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register("users", views.AccountUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("api/v1/auth/", include('djoser.urls')),
    path("api/v1/auth/", include(router.urls)),
    path('api/v1/auth/', include('users.urls')),
]
