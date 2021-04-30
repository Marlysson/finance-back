
class Calculator:

	@classmethod
	def calculate(cls, moviments):

		total = 0
		
		for moviment in moviments:
			total += moviment.value()

		return total