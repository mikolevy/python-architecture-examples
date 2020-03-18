from rest_framework.viewsets import ModelViewSet

from examples.anemic_model import Product
from examples.anemic_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
