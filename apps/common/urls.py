from django.urls import path, include
from .crud_views import *
from rest_framework.authtoken import views


app_name = "common"
API_URL_PREFIX = "api/"

urlpatterns = [
    path('categories/', CategoryView.as_view()),    
    path('categories/<int:id>/', CategoryViewId.as_view()),
    path('subcategories/', SubcategoryView.as_view()),        
    path('subcategories/<int:id>/', SubcategoryViewId.as_view()),
    path('products/', ProductView.as_view()),          
    path('products/<int:id>/', ProductViewId.as_view()),  
    path('change-password/', ChangePasswordView.as_view()),
    path('upload-categories/', UploadCategoryCSV.as_view()),
    path('upload-subcategories/', UploadSubCategoryCSV.as_view()),
    path('upload-product/', UploadProductCSV.as_view())
]
