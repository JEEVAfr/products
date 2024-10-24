from apps.common.models.base import *

class Category(BaseModel):

    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Subcategory(BaseModel):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

class Product(BaseModel):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    brand = models.CharField(max_length=255)
    color = models.CharField(max_length=100)
    review = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)

    def __str__(self) -> str:
        return self.name