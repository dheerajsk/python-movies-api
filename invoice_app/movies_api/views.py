from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .serializers import ItemSerializer, InvoiceSerializer, UserSerializer
import json
import jwt
import datetime
from bson import ObjectId
from django.conf import settings
from .models import User, Invoice,Movie
from django.core.exceptions import ObjectDoesNotExist

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

class MovieDisplay(View):
    def get(self, request):
        movies = Movie.objects.all()
        # Render the movies on the webpage or template and provide a link to the detailed Movie Details Page for each movie
        return render(request, 'movie_display.html', {'movies': movies})

class MovieFiltering(View):
    def get(self, request):
        genre = request.GET.get('genre')
        language = request.GET.get('language')
        location = request.GET.get('location')
        rating = request.GET.get('rating')

        movies = Movie.objects.all()

        if genre:
            movies = movies.filter(genre=genre)

        if language:
            movies = movies.filter(language=language)

        if location:
            # Apply location filtering logic here if you have it as a field in the Movie model
            pass

        if rating:
            movies = movies.filter(rating=rating)

        # Render the filtered movies on the webpage or template
        return render(request, 'movie_filtering.html', {'movies': movies})


# class GetAllInvoices(View):
#     def get(self, request):
#         invoices = Invoice.objects.all()
#         invoice_serializer = InvoiceSerializer(invoices, many=True)
#         return JsonResponse(invoice_serializer.data, safe=False)

# class AddInvoice(View):
#     def post(self, request):
#         invoice_data = json.loads(request.body)
#         invoice_data["invoice_id"]= Invoice.objects.count() + 1

#         invoice_serializer = InvoiceSerializer(data=invoice_data)
#         if invoice_serializer.is_valid():
#             invoice = invoice_serializer.save()  # This will save the data to the database and return the saved instance
#             saved_invoice_serializer = InvoiceSerializer(invoice)
#             return JsonResponse(saved_invoice_serializer.data, status=201)
#         else:
#             return HttpResponseBadRequest()

# class GetInvoice(View):
#     def get(self, request, invoice_id):
#         try:
#             invoice = Invoice.objects.get(_id=ObjectId(invoice_id))
#         except ObjectDoesNotExist:
#             return JsonResponse({"error": "Invoice not found"}, status=404)
        
#         invoice_serializer = InvoiceSerializer(invoice)
#         return JsonResponse(invoice_serializer.data, safe=False)

# class InvoiceItemAdd(View):
#     def post(self, request, invoice_id):
#         invoice_id = ObjectId(invoice_id)
#         invoice = get_object_or_404(Invoice, _id=ObjectId(invoice_id))

#         item_data = json.loads(request.body)
#         item_data['invoice_id'] = ObjectId(invoice._id)
#         item_serializer = ItemSerializer(data=item_data)

#         if item_serializer.is_valid():
#             item = item_serializer.save()
#             return JsonResponse(ItemSerializer(item).data, status=201)
#         else:
#             return HttpResponseBadRequest()


class UserSignUp(View):
    def post(self, request):
        user_data=json.loads(request.body)
        
        #Validate data using serializer
        user_serialized=UserSerializer(data=user_data)
        if(user_serialized.is_valid()):
            user_instance = user_serialized.save()

            return JsonResponse(user_serialized.data, status=201)
        else:
            return HttpResponseBadRequest()

class UserSignIn(View):
    def post(self, request):
        user_data = json.loads(request.body)
        try:
            # Fetch user from database
            user = User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            # User not found in database
            return HttpResponseBadRequest()

        # Check password - this should be improved because storing and comparing passwords as plain text is not secure
        if user.password == user_data["password"]:
            # Generate a token with the user's email and an expiration time
            token = jwt.encode({
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Expiration time
            }, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({"token": token}, status=200)
        else:
            # Password didn't match
            return HttpResponseBadRequest()