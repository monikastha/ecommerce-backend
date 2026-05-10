# adminperson/views.py

from rest_framework import viewsets
from .models import AdminPerson
from .serializers import AdminPersonSerializer


class AdminPersonViewSet(viewsets.ModelViewSet):

    queryset = AdminPerson.objects.all()
    serializer_class = AdminPersonSerializer