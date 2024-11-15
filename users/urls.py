from django.urls import path
from .views import MyTokenObtainPairView, signup, login, getRoutes
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', getRoutes, name='routes'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
