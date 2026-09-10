from rest_framework import generics, permissions
from .models import Category, Position
from .serializers import CategorySerializer, PositionSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Admin gets all, others get active categories only
        if self.request.user.is_authenticated and getattr(self.request.user, 'role', None) == 'ADMIN':
            return Category.objects.all().order_by('order', 'id')
        return Category.objects.filter(is_active=True).order_by('order', 'id')

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class PositionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PositionSerializer

    def get_queryset(self):
        queryset = Position.objects.all().order_by('order', 'id')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

