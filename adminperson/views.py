from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AdminPerson
from .serializers import AdminPersonSerializer, AdminPersonCreateSerializer


class AdminPersonListCreateView(generics.ListCreateAPIView):
    queryset = AdminPerson.objects.select_related('user').all()
    permission_classes = [permissions.IsAdminUser]   # Only admins can access

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminPersonCreateSerializer
        return AdminPersonSerializer


class AdminPersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminPerson.objects.select_related('user').all()
    serializer_class = AdminPersonSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


class AdminPersonMeView(APIView):
    """Get current logged-in admin's profile"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            admin_person = AdminPerson.objects.select_related('user').get(user=request.user)
            serializer = AdminPersonSerializer(admin_person)
            return Response(serializer.data)
        except AdminPerson.DoesNotExist:
            return Response(
                {"detail": "Admin profile not found. Contact super admin."}, 
                status=status.HTTP_404_NOT_FOUND
            )