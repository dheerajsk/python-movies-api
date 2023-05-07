from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .serializers import InvoiceItemSerializer, InvoiceSerializer, UserSerializer
import json

# Create your views here.

users=[]
invoices = [
    {
        "invoice_id": 1,
        "client_name": "John Doe",
        "date": "2023-05-01",
        "items": [
            {"item_id": 1, "invoice_id": 1, "desc": "Product A", "quantity": 2, "rate": 100},
            {"item_id": 2, "invoice_id": 1, "desc": "Product B", "quantity": 1, "rate": 200},
        ],
    },
    {
        "invoice_id": 2,
        "client_name": "Jane Smith",
        "date": "2023-05-02",
        "items": [
            {"item_id": 3, "invoice_id": 2, "desc": "Product A", "quantity": 5, "rate": 100},
            {"item_id": 4, "invoice_id": 2, "desc": "Product C", "quantity": 3, "rate": 150},
        ],
    },
    {
        "invoice_id": 3,
        "client_name": "Michael Brown",
        "date": "2023-05-03",
        "items": [
            {"item_id": 5, "invoice_id": 3, "desc": "Product B", "quantity": 2, "rate": 200},
            {"item_id": 6, "invoice_id": 3, "desc": "Product D", "quantity": 1, "rate": 250},
        ],
    },
    {
        "invoice_id": 4,
        "client_name": "Emma Johnson",
        "date": "2023-05-04",
        "items": [
            {"item_id": 7, "invoice_id": 4, "desc": "Product A", "quantity": 1, "rate": 100},
            {"item_id": 8, "invoice_id": 4, "desc": "Product C", "quantity": 2, "rate": 150},
            {"item_id": 9, "invoice_id": 4, "desc": "Product D", "quantity": 1, "rate": 250},
        ],
    },
    {
        "invoice_id": 5,
        "client_name": "James Williams",
        "date": "2023-05-05",
        "items": [
            {"item_id": 10, "invoice_id": 5, "desc": "Product A", "quantity": 3, "rate": 100},
            {"item_id": 11, "invoice_id": 5, "desc": "Product B", "quantity": 1, "rate": 200},
            {"item_id": 12, "invoice_id": 5, "desc": "Product C", "quantity": 2, "rate": 150},
        ],
    },
]


class GetAllInvoices(View):
    def get(self, request):
        invoice_serializer = InvoiceSerializer(invoices, many=True)
        return JsonResponse(invoice_serializer.data, safe=False)

class GetInvoice(View):
    def get(self, request, invoice_id):
        for invoice in invoices:
            if invoice["id"] == invoice_id:
                invoice_serializer = InvoiceSerializer(invoice)
                return JsonResponse(invoice_serializer.data, safe=False)
        return JsonResponse({"error": "Invoice not found"}, status=404)
    
class InvoiceItemGet(View):
    def put(self, request, invoice_id, item_id):
        for index, invoice in enumerate(invoices):
            if invoice["invoice_id"] == invoice_id:
                for item_index, item in enumerate(invoice['items']):
                    if item["item_id"] == item_id:
                        return JsonResponse(item, status=200)
        return HttpResponseBadRequest()

class InvoiceItemUpdate(View):
    def put(self, request, item_id):
        #Parse data from req.body.
        item_data=json.loads(request.body)
        #Validate data
        item_serialized=InvoiceItemSerializer(data=item_data)
        if(item_serialized.is_valid()):
            # Find the invoice to update
            item_to_update=None
            for index, invoice in enumerate(invoices):
                if(invoice["invoice_id"]==item_data["invoice_id"]):
                    for item_index, item in enumerate(invoice.items):
                        if(item["item_id"]==item_id):
                            item_to_update=item
                            break
            
            # if data found, update it.
            if(item_to_update):
                invoices[index].items[item_index]=item_serialized.data
                return JsonResponse(item_serialized.data, status=200)
            
        return HttpResponseBadRequest()

class UserSignUp(View):
    def post(self, request):
        user_data=json.loads(request.body)
        user_data["user_id"]=len(users)+1
        
        #Validate data using serializer
        user_serialized=UserSerializer(data=user_data)
        if(user_serialized.is_valid()):
            users.append(user_serialized.data)

            return JsonResponse(user_serialized.data, status=201)
        else:
            return HttpResponseBadRequest()

class UserSignIn(View):
    def post(self, request):
        user_data=json.loads(request.body)
        print(user_data)
        print(user_data["email"])
        for index, item in enumerate(users):
                if(item["email"]==user_data["email"] and item["password"]==user_data["password"]):
                    return JsonResponse("Login is Successful", safe=False,status=200)
        return HttpResponseBadRequest()