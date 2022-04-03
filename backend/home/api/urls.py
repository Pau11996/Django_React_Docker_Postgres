from django.urls import path, include

#from rest_framework import routers
from .views import CategoryListView, ProductsViewSet, CategoryDetailView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# router = routers.SimpleRouter()
# # router.register('category', CategoryListView, basename='category')
# router.register('products', ProductsViewSet, basename='blogpost')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('category/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

]
# urlpatterns += router.urls