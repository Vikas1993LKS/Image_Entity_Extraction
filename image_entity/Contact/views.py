from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import ContactSerializer
from .models import Contact

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('person_name')
    serializer_class = ContactSerializer