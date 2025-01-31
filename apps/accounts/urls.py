from django.urls import path
from .views import CreateChanel, DeleteChanel, GetChanel
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_chanel/', CreateChanel.as_view(), name='create_channel'),
    path('delete/<int:pk>/', DeleteChanel.as_view(), name='delete'),
    path('get/', GetChanel.as_view(), name='get'),
]
