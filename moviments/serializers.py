from rest_framework import serializers

from .models import Moviment

class MovimentSerializer(serializers.ModelSerializer):

	description = serializers.CharField(
		required=True, 
		allow_null=False, 
		error_messages={
			"required": "A descrição é obrigatória.", 
			"blank": "A descrição deve ser preenchida."
		}
	)

	amount = serializers.DecimalField(
		min_value=1,
		max_digits=7, 
		decimal_places=2,
		error_messages={
			"required": "O valor é obrigatório.",
			"min_value": "O valor deve ser maior que 0."
		}
	)

	operation = serializers.ChoiceField(
		choices=["INCOME", "EXPENSE"], 
		allow_blank=False,
		error_messages={
			"required": "A operação é obrigatória."
		}
	)

	class Meta:
		model = Moviment
		fields = '__all__'