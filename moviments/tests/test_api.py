from django.urls import reverse
from rest_framework.test import APITestCase
import unittest
from ..models import Moviment

class MovimentsAPITest(APITestCase):

	maxDiff = None

	def setUp(self):
		self.url = reverse('moviment-list')

	def test_should_list_a_simple_moviment_created(self):

		moviment = Moviment(description="Lanche", amount=245, operation="INCOME")
		moviment.save()

		response = self.client.get(self.url, format="json")

		self.assertEqual(response.json(), [{'id': 1, 'description': 'Lanche', 'amount': '245.00', 'operation': 'INCOME'}])

	def test_should_show_errors_when_some_fields_isnt_filled(self):

		# Validation for 'DESCRIPTION' field

		moviment = {'amount': 100, 'operation': 'INCOME'}
		response = self.client.post(self.url, moviment, format="json")

		errors = response.json()
		self.assertEqual(errors["description"][0], "A descrição é obrigatória.")

		moviment = {'description': '', 'amount': 65.00, 'operation': 'INCOME'}
		response = self.client.post(self.url, moviment, format="json")

		errors = response.json()
		self.assertEqual(errors["description"][0], "A descrição deve ser preenchida.")

		# Validation for 'AMOUNT' field

		moviment = {'description': 'Livros', 'operation': 'INCOME'}
		response = self.client.post(self.url, moviment, format="json")

		errors = response.json()
		self.assertEqual(errors["amount"][0], "O valor é obrigatório.")

		moviment = {'description': 'Livros', 'amount': 0, 'operation': 'INCOME'}
		response = self.client.post(self.url, moviment, format="json")

		errors = response.json()
		self.assertEqual(errors["amount"][0], "O valor deve ser maior que 0.")

		# Validation for 'OPERATION' field

		moviment = {'description': 'Livros', 'amount': 100}
		response = self.client.post(self.url, moviment, format="json")

		errors = response.json()
		self.assertEqual(errors["operation"][0], "A operação é obrigatória.")

	def test_should_add_two_simple_income_moviments(self):
		
		moviment = {'description': 'Livros', 'amount': 2000, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")
		
		moviment = {'description': 'Livros', 'amount': 2500, 'operation': 'EXPENSE'}
		r = self.client.post(self.url, moviment, format="json")
		
		response = self.client.get(self.url, format="json")
		
		correct_response_api = [
			{'id': 1, 'description': 'Livros', 'amount': '2000.00', 'operation': 'INCOME'},
			{'id': 2, 'description': 'Livros', 'amount': '2500.00', 'operation': 'EXPENSE'}
		]

		self.assertListEqual(response.json(), correct_response_api)

	def test_should_add_a_couple_of_moviments(self):

		moviment = {'description': 'Livros', 'amount': 100, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 250, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 1200, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")	

		moviment = {'description': 'Livros', 'amount': 3240, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		response = self.client.get(self.url, format="json")

		correct_response_api = [
			{'id': 1, 'description': 'Livros', 'amount': '100.00', 'operation': 'INCOME'},
			{'id': 2, 'description': 'Livros', 'amount': '250.00', 'operation': 'INCOME'},
			{'id': 3, 'description': 'Livros', 'amount': '1200.00', 'operation': 'INCOME'},
			{'id': 4, 'description': 'Livros', 'amount': '3240.00', 'operation': 'INCOME'},
		]

		self.assertListEqual(response.json(), correct_response_api)

	def test_should_process_a_moviments_with_different_types(self):

		moviment = {'description': 'Livros', 'amount': 1000, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 2000, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 500, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")	

		moviment = {'description': 'Livros', 'amount': 150, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")

		response = self.client.get(self.url, format="json")

		correct_response_api = [
			{'id': 1, 'description': 'Livros', 'amount': '1000.00', 'operation': 'INCOME'},
			{'id': 2, 'description': 'Livros', 'amount': '2000.00', 'operation': 'EXPENSE'},
			{'id': 3, 'description': 'Livros', 'amount': '500.00', 'operation': 'INCOME'},
			{'id': 4, 'description': 'Livros', 'amount': '150.00', 'operation': 'EXPENSE'},
		]

		self.assertEqual(response.json(), correct_response_api)
	
	def test_should_return_statistics_from_moviments(self):

		moviment = {'description': 'Livros', 'amount': 1000, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 2000, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'description': 'Livros', 'amount': 500, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		response = self.client.get(reverse('statistics')).json()

		response_data = {
			"balance": -500.0, 
			"incomes": 1500.0,
			"expenses": -2000.0
		}

		self.assertDictEqual(response_data, response)