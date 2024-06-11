from django.urls import path

from . import views

urlpatterns = [
    path('jwt/create/', view=views.UserTokenObtainPairView.as_view()),
    path('jwt/refresh/', view=views.UserTokenRefreshView.as_view()),
    path('jwt/verify/', view=views.UserTokenVerifyView.as_view()),
    path('logout/', view=views.LogoutView.as_view())
]
