from rest_framework import serializers

from examples.anemic_model import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
