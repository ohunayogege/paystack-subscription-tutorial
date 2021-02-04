from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']
