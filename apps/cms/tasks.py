import io
import csv
import logging
from celery import shared_task
from apps.common.models.base import *
from .serializers import *
from rest_framework import status
from .views import *


logger = logging.getLogger(__name__)


def batched_query(queryset, batch_size=10): # retrive the data in batches

    total = queryset.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        for entry in queryset[start:end]:
            yield entry

@shared_task
def celery_category(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')

    data_chunk = []

    for row in reader:

        if not row or len(row) < 4:
            continue

        category_data = Category(
            name=row[0],
            description=row[1],
            slug=row[2],
            status=row[3].lower() == 'true',
        )
        
        data_chunk.append(category_data)

        if len(data_chunk) >= batch_size:
            save_categories(data_chunk)
            data_chunk = []  

    if data_chunk:
        save_categories(data_chunk)

    return {'status': 'success', 'message': 'Categories uploaded successfully'}

def save_categories(chunk):
    try:
        Category.objects.bulk_create(chunk)
    except Exception as e:
        print(f"Error during bulk create: {e}")


@shared_task
def celery_subcategory(file_data, batch_size=10):

    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')

    data_chunk = []
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

        data_chunk.append(subcategory_data)

        if len(data_chunk) >= batch_size:
            save_subcategories(data_chunk)
            data_chunk = []

    
    if data_chunk:
        save_subcategories(data_chunk)

    if errors:
        return {'status': 'failed', 'errors': errors}
    
    return {'status': 'success', 'message': 'Subcategories uploaded successfully'}


def save_subcategories(chunk):
    try:
        subcategory_instances = [Subcategory(
            category=Category.objects.get(id=data['category']),
            name=data['name'],
            description=data['description'],
            slug=data['slug'],
            status=data['status']
        ) for data in chunk]

        Subcategory.objects.bulk_create(subcategory_instances)
    except Exception as e:
        print(f"Error during bulk create: {e}")


@shared_task
def celery_product(file_data, batch_size=10):
    io_string = io.StringIO(file_data)
    reader = csv.reader(io_string, delimiter=',')

    errors = []
    data_chunk = []
    for row in reader:
        if not row:
            continue
            
        if len(row) < 9:
            errors.append({'error': f'Row does not contain enough data: {row}'})
            continue

        try:
            category = Category.objects.get(id=row[0])  
        except Category.DoesNotExist:
            errors.append({'error': f'Category with ID {row[0]} does not exist'})
            continue

        try:
            subcategory = Subcategory.objects.get(id=row[1])  
        except Subcategory.DoesNotExist:
            errors.append({'error': f'Subcategory with ID {row[1]} does not exist'})
            continue

        
        product_data = {
            'category': category, 
            'subcategory': subcategory,  
            'name': row[2],
            'description': row[3],
            'status': row[4].lower() == 'true',  
            'brand': row[5],
            'color': row[6],
            'review': row[7],
            'rating': row[8],
        }

        data_chunk.append(product_data)

        if len(data_chunk) >= batch_size:
            save_products(data_chunk)
            data_chunk = []

    if data_chunk:
        save_products(data_chunk)

    if errors:
        return {'status': 'failed', 'errors': errors}

    return {'status': 'success', 'message': 'Products uploaded successfully'}


def save_products(chunk):
    try:

        product_instances = [
            Product(
                category=data['category'], 
                subcategory=data['subcategory'],  
                name=data['name'],
                description=data['description'],
                status=data['status'],
                brand=data['brand'],
                color=data['color'],
                review=data['review'],
                rating=data['rating']
            )
            for data in chunk
        ]
        
        Product.objects.bulk_create(product_instances)
    except Exception as e:
        print(f"Error during bulk create: {e}")
