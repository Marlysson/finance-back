from rest_framework import serializers

from .models import Moviment

class MovimentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Moviment
		fields = '__all__'