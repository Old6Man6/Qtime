from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from branches.models import Service, Branch
from branches.serializers import ServiceSerializer, BranchSerializer


class ServiceViewSet(ModelViewSet):
    """
    ViewSet for managing services.
    - Admins can create, update, delete.
    - Users can view services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUser()]


class BranchViewSet(ModelViewSet):
    """
    ViewSet for managing branches.
    - Admins can create, update, delete.
    - Authenticated users (and unauthenticated, if desired) can view.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]  # anyone can read
        return [IsAdminUser()]  # only admin can write