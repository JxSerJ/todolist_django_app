from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.RegexField(regex='^[\w.@+-]+$', required=True, max_length=150, min_length=1,
                                      allow_null=False, allow_blank=False)
    first_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(required=True, max_length=128)

    def validate_username(self, username):
        """Validate username existence"""
        if self.Meta.model.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'User "{username}" already exists')
        else:
            return username

    @staticmethod
    def validate_password(password):
        """Standard django password validator"""
        validate_password(password)
        return password

    def validate(self, data):
        """Check password and password_repeat"""
        if data.get('password') == self.initial_data.get('password_repeat'):
            return data
        raise serializers.ValidationError({'password_repeat': ['Passwords does not match'],
                                           'password': ['Passwords does not match']})

    def create(self, validated_data):
        """Create user and write it into database"""
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=1)
    password = serializers.CharField(required=True, min_length=1)

    def validate_username(self, username):
        """Validate username existence"""
        if not self.Meta.model.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'User "{username}" does not exist')
        else:
            return username

    class Meta:
        model = User
        fields = ['username', 'password']


class RetrieveUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    username = serializers.RegexField(regex='^[\w.@+-]+$', required=False, max_length=150, min_length=1,
                                      allow_null=False, allow_blank=False)
    first_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_username(self, username):
        request = self.context.get('request', None)
        if request:
            current_user = request.user
        else:
            raise serializers.ValidationError({'username': ['Login error']})

        """Validate username existence"""
        if self.Meta.model.objects.filter(username=username).exists() and current_user.username != username:
            raise serializers.ValidationError(f'User "{username}" already exists')
        else:
            return username

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
