from rest_framework import serializers

from .models import Product
class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_type', 'is_available', 'stock', 'stock_status']

    def get_stock_status(self, obj):
        if obj.stock == 0:
            return None
        elif obj.stock <= 2:
            return "Stock needs to be refilled"
        else:
            return obj.stock