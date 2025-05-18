from goods.models import SubCategory
from .models import Category, SubCategory

def categories(request):
    return {
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        
    }