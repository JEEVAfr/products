import pandas as pd
from .serializers import *
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
import csv, io
from django.core.files.storage import FileSystemStorage
from .tasks import *

class CustomPagination(PageNumberPagination):

    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  

class CategoryView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewId(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        
        category = get_object_or_404(Category, id=id)
        category.delete()
        
        return Response({
            "status": "success",
            "message": "Category deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class SubcategoryView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):

        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class SubcategoryViewId(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        subcategory = get_object_or_404(Subcategory, id=id)
        serializer = SubcategorySerializer(subcategory)
        
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    
    def patch(self, request, id):

        subcategory = get_object_or_404(Subcategory, id=id)
        serializer = SubcategorySerializer(instance=subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        subcategory = get_object_or_404(Subcategory, id=id)
        subcategory.delete()
        
        return Response({
            "status": "success",
            "message": "Subcategory deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ProductView(APIView):

    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class ProductViewId(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, id):
        
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        
        product = get_object_or_404(Product, id=id)
        product.delete()
        
        return Response({
            "status": "success",
            "message": "Product deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"status": "Success", "message": "Password updated."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"status": "Failed", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class UploadCategoryCSV(APIView):

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded_file = csv_file.read().decode('utf-8')
        
        task = celery_category.delay(decoded_file)

        return Response({'message': 'File is being processed'}, status=status.HTTP_202_ACCEPTED)
    

class UploadSubCategoryCSV(APIView):

    def post(self, request):

        if 'file' not in request.FILES:
            return Response({'error' : 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded_file = csv_file.read().decode('-utf-8')

        task = celery_subcategory.delay(decoded_file)

        return Response({'message' : 'File is being processed'}, status=status.HTTP_202_ACCEPTED)


class UploadProductCSV(APIView):

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded_file = csv_file.read().decode('-utf-8')
        
        task = celery_product.delay(decoded_file)

        return Response({'message' : 'File is being processed'}, status=status.HTTP_202_ACCEPTED)

