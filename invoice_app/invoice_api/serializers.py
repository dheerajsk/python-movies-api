from rest_framework import serializers
from .models import User
from rest_framework import serializers

class InvoiceItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    desc = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()
    rate = serializers.DecimalField(max_digits=10, decimal_places=2)

class InvoiceSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    client_name = serializers.CharField(max_length=60)
    items = InvoiceItemSerializer(many=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'