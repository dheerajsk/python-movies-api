from django.urls import path
from .views import GetAllInvoices, GetInvoice, InvoiceItemGet, InvoiceItemUpdate
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('invoices/', csrf_exempt(GetAllInvoices.as_view()), name='get_all_invoices'),
    path('invoices/<int:invoice_id>/', csrf_exempt(GetInvoice.as_view()), name='get_invoice'),
    path('invoices/<int:invoice_id>/item/<int:item_id>', csrf_exempt(InvoiceItemGet.as_view()), name='item_get'),
    path('items/<int:item_id>/update', csrf_exempt(InvoiceItemUpdate.as_view()), name='item_get'),
]
