from django.urls import path

from market.views import ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, \
    ProductDestroyAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product_list'),
    path('create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('<int:pk>/', ProductRetrieveAPIView.as_view(), name='product_detail'),
    path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDestroyAPIView.as_view(), name='product_delete')
]
