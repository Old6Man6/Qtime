from django.urls import path, include
from rest_framework.routers import DefaultRouter
from branches.views import BranchViewSet, ServiceViewSet

# Router creation
router = DefaultRouter()

# Register ViewSets with router
router.register('branches', BranchViewSet, basename='branch')
router.register('services', ServiceViewSet, basename='service')

# Include auto-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]