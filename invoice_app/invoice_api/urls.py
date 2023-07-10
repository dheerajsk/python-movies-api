from django.urls import path
from .views import GetAllInvoices, GetInvoice, AddInvoice, UserSignIn, UserSignUp, InvoiceItemAdd
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('invoices/<str:invoice_id>', csrf_exempt(GetInvoice.as_view()), name='get_invoice'),
    path('invoices', csrf_exempt(GetAllInvoices.as_view()), name='get_all_invoices'),
    path('invoices/new', csrf_exempt(AddInvoice.as_view()), name='add_invoices'),
    path('invoices/<str:invoice_id>/items', csrf_exempt(InvoiceItemAdd.as_view()), name='item_add'),
    path('user/signup', csrf_exempt(UserSignUp.as_view()), name='signup'),
    path('user/signin', csrf_exempt(UserSignIn.as_view()), name='signin'),
    
]
