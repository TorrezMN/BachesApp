from random import choice
from rest_framework import serializers
# Importing Models
from app_db.models import User
from app_db.models import Caracteristicas
from app_db.models import Registro


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class test_data(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


class Caracteristicas_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristicas
        fields = '__all__'


class Registro_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email']

        )
        try:
            user.set_password(validated_data['password'])
            user.save()
            return (user)
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)
