from rest_framework import viewsets

from .serializers import MovimentSerializer
from .models import Moviment

class MovimentView(viewsets.ModelViewSet):
	queryset = Moviment.objects.all()
	serializer_class = MovimentSerializer