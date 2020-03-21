from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import  CreateUserView, LoginView, ResetPassword

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user', CreateUserView.as_view(),),
    path('login', LoginView.as_view(), ),
    path('reset-password', ResetPassword.as_view(), name='reset_password'),
]

