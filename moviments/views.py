from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MovimentSerializer
from .models import Moviment

from .calculator import Calculator

class MovimentView(viewsets.ModelViewSet):
	queryset = Moviment.objects.all()
	serializer_class = MovimentSerializer

class StatisticsView(APIView):

	def get(self, request, format="json"):

		moviments = Moviment.objects.all()
		incomes = Moviment.objects.filter(operation="INCOME")
		expenses = Moviment.objects.filter(operation="EXPENSE")

		data = {
			"balance": Calculator.calculate(moviments),
			"incomes": Calculator.calculate(incomes),
			"expenses": Calculator.calculate(expenses)
		}

		return Response(data=data, status=status.HTTP_200_OK)