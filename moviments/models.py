from django.db import models

class Moviment(models.Model):

	TYPES = [
		("EXPENSE", "EXPENSE"),
		("INCOME", "INCOME")
	]	

	description = models.CharField(max_length=255, default='')
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	operation = models.CharField(max_length=7, choices=TYPES)

	def value(self):

		operations = {
			"EXPENSE": (-1),
			"INCOME": (1)
		}

		moviment_type_operation = operations[self.operation]

		return moviment_type_operation * self.amount

	class Meta:
		db_table = "moviment"