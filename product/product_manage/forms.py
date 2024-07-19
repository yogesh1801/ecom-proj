from django.forms import ModelForm
from product_manage.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','category','stock','price']