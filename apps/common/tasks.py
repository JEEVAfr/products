import io
import csv
import logging
from celery import shared_task
from apps.common.models.base import *
from .serializers import *
from rest_framework import status

logger = logging.getLogger(__name__)

@shared_task
def process_category(file_data):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')
    
    errors = []
    for row in reader:
        if not row:
            continue
        
        if len(row) < 4:
            errors.append(f'Row does not contain enough data: {row}')
            continue

        category_data = {
            'name': row[0],
            'description': row[1],
            'slug': row[2],
            'status': row[3].lower() == 'true',
        }

        serializer = CategorySerializer(data=category_data)
        if serializer.is_valid():
            serializer.save()
        else:
            errors.append(serializer.errors)

    if errors:
        return {'status': 'failed', 'errors': errors}
    
    return {'status': 'success', 'message': 'Categories uploaded successfully'}

@shared_task
def process_subcategory(file_data):

    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')

    errors = []
    for row in reader:

        if not row:
            continue

        if len(row) < 5: 
            errors.append(f'Row does not contain enough data: {row}')
            continue
            
        try:
            category = Category.objects.get(id=row[0])
        except Category.DoesNotExist:
            errors.append(f'Category with ID {row[0]} does not exist')
            continue

        subcategory_data = {
                'category': category.id,
                'name': row[1],
                'description': row[2],
                'slug': row[3],
                'status': row[4].lower() == 'true', 
            }

        serializer = SubcategorySerializer(data = subcategory_data)
        if serializer.is_valid():
            serializer.save()
        else:
            errors.append(serializer.errors)

        if errors:
            return {'status': 'failed', 'errors': errors}

    return {'status': 'success', 'message': 'Subcategories uploaded successfully'}


@shared_task
def process_product(file_data):

    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')

    errors = []
    for row in reader:

        if not row:
            continue
            
        if len(row) < 9:
            return errors.append({'error': f'Row does not contain enough data: {row}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=row[0])
        except Category.DoesNotExist:
            return errors.append({'error': f'Category with ID {row[0]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = Subcategory.objects.get(id=row[1])
        except Subcategory.DoesNotExist:
            return errors.append({'error': f'Subcategory with ID {row[1]} does not exist'}, status=status.HTTP_400_BAD_REQUEST)


        product_data = {
                'category': category.id, 
                'subcategory': subcategory.id,  
                'name': row[2],
                'description': row[3],
                'status': row[4].lower() == 'true',  
                'brand': row[5],
                'color': row[6],
                'review': row[7],
                'rating': row[8],
        }

        serializer = ProductSerializer(data=product_data)

        if serializer.is_valid():
            serializer.save()
        else:
            errors.append(serializer.errors)

        if errors:
            return {'status': 'failed', 'errors': errors}

    return {'status': 'success', 'message': 'Subcategories uploaded successfully'}



