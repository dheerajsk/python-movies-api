from rest_framework import serializers
from .models import User, Invoice, Item
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

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('_id','desc', 'quantity', 'rate')

class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)  # indicates that items field is a list of items

    class Meta:
        model = Invoice
        fields = ('_id','client_name', 'date', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(invoice=invoice, **item_data)
        return invoice