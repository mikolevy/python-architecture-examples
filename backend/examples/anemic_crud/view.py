from rest_framework.viewsets import ModelViewSet

from examples.anemic_crud.model import Product
from examples.anemic_crud.serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
