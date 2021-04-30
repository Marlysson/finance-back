from django.test import TestCase
from ..models import Moviment
from ..calculator import Calculator

class TestMoviments(TestCase):

	def test_should_add_two_simple_income_moviments(self):

		INCOME = Moviment.TYPES[1][0]

		moviment_one = Moviment.objects.create(amount=2000, operation=INCOME)
		moviment_two = Moviment.objects.create(amount=2500, operation=INCOME)

		moviments = [ moviment_one, moviment_two ]

		total = Calculator.calculate(moviments)

		self.assertEqual(total, 4500)

	def test_should_add_a_couple_of_moviments(self):

		INCOME = Moviment.TYPES[1][0]

		moviment_one = Moviment.objects.create(amount=100, operation=INCOME)
		moviment_two = Moviment.objects.create(amount=250, operation=INCOME)
		moviment_three = Moviment.objects.create(amount=1200, operation=INCOME)
		moviment_four = Moviment.objects.create(amount=3240, operation=INCOME)

		moviments = [moviment_one ,moviment_two ,moviment_three ,moviment_four]

		total = Calculator.calculate(moviments)

		self.assertEqual(total, 4790)

	def test_should_process_a_moviments_with_different_types(self):

		EXPENSE = Moviment.TYPES[0][0]
		INCOME = Moviment.TYPES[1][0]

		moviment_one = Moviment.objects.create(amount=1000, operation=INCOME)
		moviment_two = Moviment.objects.create(amount=2000, operation=EXPENSE)
		moviment_three = Moviment.objects.create(amount=500, operation=INCOME)
		moviment_four = Moviment.objects.create(amount=150, operation=EXPENSE)

		moviments = [moviment_one ,moviment_two ,moviment_three ,moviment_four]

		total = Calculator.calculate(moviments)

		self.assertEqual(total, -650)
