from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import CommissionSettings
from .serializers import CommissionSettingsSerializer


class CommissionSettingsViewSet(viewsets.ModelViewSet):
    queryset = CommissionSettings.objects.all()
    serializer_class = CommissionSettingsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['get'], permission_classes=[])
    def current(self, request):
        settings = CommissionSettings.get_settings()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[])
    def update_settings(self, request):
        settings = CommissionSettings.get_settings()
        serializer = self.get_serializer(settings, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Commission settings updated successfully',
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
