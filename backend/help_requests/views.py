from rest_framework import viewsets, permissions
from .models import HelpRequest
from .serializers import HelpRequestSerializer


class HelpRequestViewSet(viewsets.ModelViewSet):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
