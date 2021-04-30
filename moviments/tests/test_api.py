from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import Moviment

class MovimentsAPITest(APITestCase):

	def setUp(self):
		self.url = reverse('moviment-list')

	def test_should_list_a_simple_moviment_created(self):

		moviment = Moviment.objects.create(amount=245, operation="INCOME")
		
		response = self.client.get(self.url, format="json")

		self.assertEqual(response.json(), [{'amount': '245.00', 'operation': 'INCOME'}])

	def test_should_add_two_simple_income_moviments(self):
		
		moviment = {'amount': 2000, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")
		
		moviment = {'amount': 2500, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")
		
		response = self.client.get(self.url, format="json")

		correct_response_api = [
			{'amount': '2000.00', 'operation': 'INCOME'},
			{'amount': '2500.00', 'operation': 'EXPENSE'}
		]

		self.assertEqual(response.json(), correct_response_api)

	def test_should_add_a_couple_of_moviments(self):

		moviment = {'amount': 100, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'amount': 250, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'amount': 1200, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")	

		moviment = {'amount': 3240, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		response = self.client.get(self.url, format="json")

		correct_response_api = [
			{'amount': '100.00', 'operation': 'INCOME'},
			{'amount': '250.00', 'operation': 'INCOME'},
			{'amount': '1200.00', 'operation': 'INCOME'},
			{'amount': '3240.00', 'operation': 'INCOME'},
		]

		self.assertEqual(response.json(), correct_response_api)

	def test_should_process_a_moviments_with_different_types(self):

		moviment = {'amount': 1000, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'amount': 2000, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")

		moviment = {'amount': 500, 'operation': 'INCOME'}
		self.client.post(self.url, moviment, format="json")	

		moviment = {'amount': 150, 'operation': 'EXPENSE'}
		self.client.post(self.url, moviment, format="json")

		response = self.client.get(self.url, format="json")

		correct_response_api = [
			{'amount': '1000.00', 'operation': 'INCOME'},
			{'amount': '2000.00', 'operation': 'EXPENSE'},
			{'amount': '500.00', 'operation': 'INCOME'},
			{'amount': '150.00', 'operation': 'EXPENSE'},
		]

		self.assertEqual(response.json(), correct_response_api)