from django.urls import path, include

from rest_framework import routers
from .views import CategoryListView, ProductsViewSet, CategoryDetailView

# router = routers.SimpleRouter()
# # router.register('category', CategoryListView, basename='category')
# router.register('products', ProductsViewSet, basename='blogpost')

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('category/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
]
# urlpatterns += router.urls